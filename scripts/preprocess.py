"""
Preprocess the raw data from Proliferate.
"""

import re
import pandas as pd
import networkx as nx
from pgmpy.readwrite import XMLBIFReader
from pgmpy.inference import VariableElimination
from ast import literal_eval
from pyprojroot import here


def process_survey(df_survey):
    """
    Convert raw survey data to tidy format
    """
    rows = []
    for _, row in df_survey.iterrows():
        response = literal_eval(row["response"])
        for key, value in response.items():
            rows.append({"pid": row["workerid"], "question": key, "response": value})
    return pd.DataFrame(rows)


def compute_graph_distance(A, B, model):
    """
    Get the distance between two nodes in a model's graph.
    """
    return nx.shortest_path_length(model.to_undirected(), source=A, target=B)


def process_queries(df_queries, true_models):
    """
    Given a dataframe of all the prediction phase trials, convert them to a dataframe with observed variables,
    values, query variables, and responses.
    """

    # extract the observed variable, observed value, and query variable from the stimulus
    stimulus_info = df_queries["stimulus"].apply(extract_info_from_query_stimulus)
    observed_vars, observed_vals, query_vars = list(zip(*stimulus_info))
    df_queries["observed_var"] = observed_vars
    df_queries["observed_val"] = observed_vals
    df_queries["query_var"] = query_vars

    # make sure predictions are integers, leave them as NA if they're already NA
    df_queries["prediction"] = df_queries["response"].apply(
        lambda x: int(x) if isinstance(x, str) else x
    )

    # compute correctnesses and distances
    df_queries["true_conditional_prob"] = df_queries.apply(
        lambda x: get_true_conditional_prob(
            x["observed_var"],
            x["observed_val"],
            x["query_var"],
            true_models[x["stimulusCondition"]],
        ),
        axis=1,
    )
    df_queries["is_correct"] = df_queries.apply(
        lambda x: (
            x["true_conditional_prob"]
            if x["prediction"] == 1
            else 1 - x["true_conditional_prob"] if x["prediction"] == 0 else 0
        ),
        axis=1,
    )

    # compute distances
    df_queries["distance"] = df_queries.apply(
        lambda x: compute_graph_distance(
            x["observed_var"], x["query_var"], true_models[x["stimulusCondition"]]
        ),
        axis=1,
    )

    # filter, rename, and sort columns
    df_queries = (
        df_queries[
            [
                "workerid",
                "trial_index",
                "condition",
                "stimulusCondition",
                "observed_var",
                "observed_val",
                "query_var",
                "distance",
                "true_conditional_prob",
                "response",
                "prediction",
                "is_correct",
                "rt",
            ]
        ]
        .rename(
            columns={
                "stimulusCondition": "stimulus_condition",
                "workerid": "pid",
                "rt": "response_time_ms",
                "response": "raw_response",
            }
        )
        .sort_values(by=["pid", "trial_index"])
        .reset_index(drop=True)
    )

    return df_queries


variable_names = {
    "Red": "A",
    "Green": "B",
    "Yellow": "C",
    "Blue": "D",
    "Purple": "E",
}


def extract_info_from_query_stimulus(stimulus):
    """
    Get the observed variable, observed value, and query variable from a query stimulus.
    """
    # extract the name of the observed variable
    observed_name_search = re.search(r"([A-Z]|[a-z])+(?= is on.)", stimulus)
    if observed_name_search:
        observed_val = 1
    else:
        observed_name_search = re.search(r"([A-Z]|[a-z])+(?= is off.)", stimulus)
        observed_val = 0
    if observed_name_search is None:
        raise ValueError(f"Could not find observed variable in {stimulus}")
    observed_var = variable_names[observed_name_search.group(0)]

    # extract the name of the query variable
    query_name_search = re.search(r"(?<=Is )([A-Z]|[a-z])+(?= on or off?)", stimulus)
    if query_name_search is None:
        raise ValueError(f"Could not find query variable in {stimulus}")
    query_var = variable_names[query_name_search.group(0)]

    return observed_var, observed_val, query_var


def get_true_conditional_prob(observed_var, observed_val, query_var, model):
    """
    Get the true conditional probability of the query variable given the observed variable.
    """
    ve = VariableElimination(model)
    conditional_prob = ve.query(
        [query_var], evidence={observed_var: str(observed_val)}, show_progress=False
    ).values[1]
    return conditional_prob


def main(args):
    df_raw = pd.read_csv(here(f"data/raw/{args['experiment_name']}.csv"))

    # load the true Bayes net.
    true_models = []
    for i in range(4):
        true_models.append(XMLBIFReader(here(f"data/chains/chain_{i}.xbn")).get_model())

    # filter out preload, instructions and training trials
    df_trials = df_raw[
        (df_raw["trial_type"] != "instructions")
        & (df_raw["trial_type"] != "browser-check")
        & (df_raw["trial_type"] != "preload")
        & (df_raw["trial_type"] != "initialize-microphone")
    ]
    df_survey = df_trials[
        (df_trials["trial_type"] == "survey-text")
        | (df_trials["trial_type"] == "survey-multi-choice")
    ]
    df_train = df_trials[
        (df_trials["trial_type"] != "survey-text")
        & (df_trials["trial_type"] != "survey-multi-choice")
        & (df_trials["trial_type"] != "survey-likert")
        & (~df_trials["correctAnswer"].isna())
    ]

    # filter for only prediction phase trials
    df_queries = df_trials[
        (df_trials["trial_type"] != "survey-text")
        & (df_trials["trial_type"] != "survey-multi-choice")
        & (df_trials["correctAnswer"].isna())
        & (~df_trials["stimulus"].str.contains("Correct!", na=False, regex=False))
        & (~df_trials["stimulus"].str.contains("Incorrect.", na=False, regex=False))
    ]

    # create and save query, survey, and train dataframes
    df_queries = process_queries(df_queries, true_models)
    df_queries.to_csv(
        here(f"data/processed/queries-{args['experiment_name']}.csv"), index=False
    )

    df_survey = process_survey(df_survey)
    df_survey.to_csv(
        here(f"data/processed/survey-{args['experiment_name']}.csv"), index=False
    )

    df_train = df_train.rename(
        columns={
            "rt": "response_time_ms",
            "workerid": "pid",
        }
    )
    df_train.to_csv(
        here(f"data/processed/train-{args['experiment_name']}.csv"), index=False
    )


if __name__ == "__main__":
    args = {
        "experiment_name": "final",
    }
    main(args)

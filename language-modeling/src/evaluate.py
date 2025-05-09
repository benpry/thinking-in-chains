"""
Evaluate a trained model on a range of queries
"""
from src.reasoning_model import ReasoningModel
from pgmpy.readwrite import XMLBIFReader
from pgmpy.inference import VariableElimination
import pandas as pd
from pyprojroot import here
from itertools import product
from src.utils import distance_in_graph
from src.estimator import run_markovian_scaffolded_generation

def run_evaluation(args):
    # get the variable names
    reader = XMLBIFReader(here(args["true_model_path"]))
    true_model = reader.get_model()

    # get the trained model
    model = ReasoningModel(
        pretrained_name=args["model_name"],
    )

    start_with_sep = args["start_with_sep"]

    ve = VariableElimination(true_model)
    true_conditional_probs = []
    observed_vars, observed_vals, query_vars, distances = [], [], [], []
    for observed_var, query_var in product(true_model.nodes, repeat=2):
        if observed_var == query_var:
            continue
        for observed_val in (0, 1):
            true_conditional_probs.append(
                ve.query(
                    variables=[query_var],
                    evidence={observed_var: str(observed_val)},
                    show_progress=False,
                ).values[1]
            )

            observed_vars.append(observed_var)
            observed_vals.append(observed_val)
            query_vars.append(query_var)
            distances.append(distance_in_graph(true_model, observed_var, query_var))

    estimates = run_markovian_scaffolded_generation(
        model, true_model, list(zip(observed_vars, observed_vals, query_vars)), start_with_sep=start_with_sep
    )


    df_results = pd.DataFrame(
        {
            "observed_var": observed_vars,
            "observed_val": observed_vals,
            "query_var": query_vars,
            "distance": distances,
            "true_prob": true_conditional_probs,
            **estimates
        }
    )
    
    return df_results

import networkx as nx
from random import random
from src.utils import get_probability_from_logits
from src.reasoning_model import ReasoningModel
from pgmpy.models import BayesianNetwork

def get_scaffold(true_model: BayesianNetwork, source_var: str, target_var: str) -> list:
    full_path = nx.shortest_path(
        true_model.to_undirected(), source=source_var, target=target_var
    )
    scaffold = full_path[1:-1]  # remove the source and target nodes
    return scaffold


def run_markovian_scaffolded_generation(model: ReasoningModel, true_model: BayesianNetwork, queries: list, n_samples=10, start_with_sep=False):
    layer_estimates = {}
    for readout_layer in range(model.model.config.n_layer + 1):
        this_layer_estimates = []
        for observed_var, observed_val, query_var in queries:
            scaffold = get_scaffold(true_model, observed_var, query_var)
            sample_estimates = []
            for _ in range(n_samples):
                if start_with_sep:
                    prompt = f"#\n{observed_var}={observed_val}\n"
                else:
                    prompt = f"{observed_var}={observed_val}\n"

                for scaffold_var in scaffold:
                    prompt += f"{scaffold_var}="
                    logits = model.read_out_from_layer([prompt], readout_layer)
                    prob_estimate = get_probability_from_logits(logits.squeeze())
                    next_val = 1 if random() < prob_estimate else 0
                    if start_with_sep:
                        prompt = f"#\n{scaffold_var}={next_val}\n"
                    else:
                        prompt = f"{scaffold_var}={next_val}\n"

                prompt += f"{query_var}="
                query_logits = model.read_out_from_layer([prompt], readout_layer)
                estimate = get_probability_from_logits(query_logits.squeeze())
                sample_estimates.append(estimate)

            this_layer_estimates.append(sum(sample_estimates) / len(sample_estimates))

        layer_estimates[
            f"markovian_scaff_gen_layer_{readout_layer}"
        ] = this_layer_estimates

    return layer_estimates

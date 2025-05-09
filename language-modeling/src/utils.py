import torch
import torch.nn.functional as F
import networkx as nx
from pgmpy.models import BayesianNetwork
ZERO_TOKEN = 15
ONE_TOKEN = 16


def get_probability_from_logits(logits: torch.Tensor) -> float:
    """
    Turn a dictionary of log probs into a probability estimate
    """
    log_probs = torch.tensor([logits[ZERO_TOKEN], logits[ONE_TOKEN]])
    probs = F.softmax(log_probs, dim=0)
    return probs[1].item()


def distance_in_graph(true_model: BayesianNetwork, var1: str, var2: str):
    return nx.shortest_path_length(true_model.to_undirected(), source=var1, target=var2)

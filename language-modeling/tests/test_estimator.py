import torch
import pytest
from pgmpy.models import BayesianNetwork
from src.estimator import get_scaffold
from src.reasoning_model import ReasoningModel
from src.estimator import run_markovian_scaffolded_generation
from src.utils import ZERO_TOKEN, ONE_TOKEN

def mock_read_out_from_layer(prompt, readout_layer):
    logits = torch.zeros(256)
    logits[ONE_TOKEN] = 100.0
    return logits

def test_get_scaffold():
    true_model = BayesianNetwork([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])
    scaffold = get_scaffold(true_model, "A", "E")
    assert scaffold == ["B", "C", "D"]

    scaffold = get_scaffold(true_model, "A", "C")
    assert scaffold == ["B"]

    scaffold = get_scaffold(true_model, "E", "A")
    assert scaffold == ["D", "C", "B"]

    scaffold = get_scaffold(true_model, "B", "B")
    assert scaffold == []

    scaffold = get_scaffold(true_model, "D", "B")
    assert scaffold == ["C"]

def test_markovian_scaffolded_generation():
    true_model = BayesianNetwork([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])
    model = ReasoningModel()
    model.read_out_from_layer = mock_read_out_from_layer
    queries = [("A", 0, "E"), ("A", 1, "E")]
    estimates = run_markovian_scaffolded_generation(model, true_model, queries)
    assert estimates["markovian_scaff_gen_layer_0"][0] > 0.999

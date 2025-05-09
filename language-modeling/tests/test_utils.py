from src.utils import ZERO_TOKEN, ONE_TOKEN, distance_in_graph
from transformers import AutoTokenizer
from pgmpy.models import BayesianNetwork

def test_tokens():
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    # decode the tokens
    tokens = tokenizer.encode("0")
    assert tokens[0] == ZERO_TOKEN
    tokens = tokenizer.encode("1")
    assert tokens[0] == ONE_TOKEN

    decoded = tokenizer.decode([ZERO_TOKEN])
    assert decoded[0] == "0"
    decoded = tokenizer.decode([ONE_TOKEN])
    assert decoded[0] == "1"


def test_distance_in_graph():
    true_model = BayesianNetwork([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])
    assert distance_in_graph(true_model, "A", "A") == 0
    assert distance_in_graph(true_model, "A", "B") == 1
    assert distance_in_graph(true_model, "A", "C") == 2
    assert distance_in_graph(true_model, "A", "D") == 3
    assert distance_in_graph(true_model, "B", "B") == 0
    assert distance_in_graph(true_model, "B", "C") == 1
    assert distance_in_graph(true_model, "B", "D") == 2
    assert distance_in_graph(true_model, "D", "B") == 2
    assert distance_in_graph(true_model, "E", "A") == 4
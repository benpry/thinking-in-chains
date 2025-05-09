from src.reasoning_model import ReasoningModel
from pgmpy.readwrite import XMLBIFReader
from pgmpy.inference import VariableElimination
from pyprojroot import here
from transformers import set_seed
import numpy as np


def compile_training_set(true_model_path):
    # read the true model
    reader = XMLBIFReader(here(true_model_path))
    model = reader.get_model()

    # get all adjacent variable pairs
    pairs = []
    for node in model.nodes():
        if len(model.get_parents(node)) == 0:
            continue
        parent = model.get_parents(node)[0]
        pairs.append((parent, node))
        pairs.append((node, parent))

    # get all possible combinations of values for each pair
    training_samples = []
    ve = VariableElimination(model)
    for observed_var, query_var in pairs:
        for observed_val in (0, 1):
            conditional_prob = ve.query(
                variables=[query_var],
                evidence={observed_var: str(observed_val)},
                show_progress=False,
            ).values[1]

            query_val = 1 if np.random.random() < conditional_prob else 0
            training_samples.append(
                f"{observed_var}={observed_val}\n{query_var}={query_val}"
            )

    return training_samples


def train_model(args):

    # set the random seed
    random_seed = args["random_seed"] if "random_seed" in args else 0
    set_seed(random_seed)

    # initialize the model
    model = ReasoningModel(
        args["model_config"],
        optimizer=args["optimizer"],
        optimizer_args=args["optimizer_args"],
        scheduler=args["scheduler"],
        scheduler_args=args["scheduler_args"],
        training_dataset_type=args["training_dataset_type"],
    )

    # create the training set and do the training
    training_samples = compile_training_set(args["true_model_path"])
    model.train_to_criterion(
        training_samples, threshold=args["criterion_threshold"]
    )

    # save the model
    model.save(args["model_name"] + "_criterion")
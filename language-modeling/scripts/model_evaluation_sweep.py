"""
Evaluate models with a range of parameters
"""

import os
import sys
from src.evaluate import run_evaluation
from pyprojroot import here

fixed_args = {}

variable_args_one_step = [
    {
        "true_model_path": "data/chains/chain_0.xbn",
        "model_name": "embd-256_chain-0_dataset-batch-with-separator",
        "training_dataset_type": "batch-with-separator",
        "criterion_threshold": 0.9,
        "start_with_sep": True,
    },
    {
        "true_model_path": "data/chains/chain_1.xbn",
        "model_name": "embd-256_chain-1_dataset-batch-with-separator",
        "training_dataset_type": "batch-with-separator",
        "criterion_threshold": 0.9,
        "start_with_sep": True,
    },
    {
        "true_model_path": "data/chains/chain_2.xbn",
        "model_name": "embd-256_chain-2_dataset-batch-with-separator",
        "training_dataset_type": "batch-with-separator",
        "criterion_threshold": 0.9,
        "start_with_sep": True,
    },
    {
        "true_model_path": "data/chains/chain_3.xbn",
        "model_name": "embd-256_chain-3_dataset-batch-with-separator",
        "training_dataset_type": "batch-with-separator",
        "criterion_threshold": 0.9,
        "start_with_sep": True,
    },
]

start_seed = 2024
n_seeds = 5
variable_args = []
for random_seed in range(start_seed, start_seed + n_seeds):
    for args in variable_args_one_step:
        variable_args.append({**args, "random_seed": random_seed})
        variable_args[-1]["model_name"] += f"_seed-{random_seed}_criterion"

if __name__ == "__main__":

    i = int(sys.argv[1])
    args = variable_args[i]
    if os.path.exists(f"{os.environ['MODELS_DIR']}/{args['model_name']}"):
        df_results = run_evaluation({**fixed_args, **args})
        df_results.to_csv(here(f"data/results/evaluation_model-{args['model_name']}.csv"), index=False)
    else:
        print(f"model not found: {args['model_name']}")

"""
Train a bunch of models with different parameters
"""

import sys
from torch.optim import Adam
from torch.optim.lr_scheduler import LinearLR
from src.train import train_model

fixed_args = {
    "model_config": {
        "vocab_size": 257,
        "n_positions": 512,
        "n_embd": 256,
        "n_layer": 8,
        "n_head": 2,
    },
    "optimizer": Adam,
    "optimizer_args": {"lr": 5e-5},
    "scheduler": LinearLR,
    "scheduler_args": {},
    "criterion": True,
    "training_dataset_type": "batch-with-separator",
    "criterion_threshold": 0.9,
}

variable_args_one_step = [
    {
        "true_model_path": "data/chains/chain_0.xbn",
        "model_name": "embd-256_chain-0_dataset-batch-with-separator",
    },
    {
        "true_model_path": "data/chains/chain_1.xbn",
        "model_name": "embd-256_chain-1_dataset-batch-with-separator",
    },
    {
        "true_model_path": "data/chains/chain_2.xbn",
        "model_name": "embd-256_chain-2_dataset-batch-with-separator",
    },
    {
        "true_model_path": "data/chains/chain_3.xbn",
        "model_name": "embd-256_chain-3_dataset-batch-with-separator",
    },
]

start_seed = 2024
n_seeds = 5

variable_args = []
for random_seed in range(start_seed, start_seed + n_seeds):
    for args in variable_args_one_step:
        variable_args.append({**args, "random_seed": random_seed})
        variable_args[-1]["model_name"] += f"_seed-{random_seed}"

if __name__ == "__main__":

    i = sys.argv[1]
    args = variable_args[int(i)]
    train_model({**fixed_args, **args})

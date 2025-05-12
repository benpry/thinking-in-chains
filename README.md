# Thinking fast, slow, and everywhere in between in humans and language models

This repo contains code and data for the paper "Thinking fast, slow, and everywhere in between in 
humans and language models" by Prystawski and Goodman, presented at CogSci 2025.

The code to reproduce our analyses can be found in the `scripts` directory. `preprocess.py` 
preprocesses the human data. `MainAnalyses.qmd` fits the models, `MakeFigures.qmd` makes figures,
and `IllustrativePlots.qmd` makes the illustrative plots in Figure 2. 

The `experiment` directory contains the JsPsych code for our experiment and `data` contains the data.

the `language-modeling` directory contains code for training language models and getting probability estimates.
To run it, you should navigate to that directory and install the module in `src/` using

```
pip install -e .
```

Next, you can run `scripts/model_training_sweep.py` and `scripts/model_evaluation_sweep.py` to train
all of the models and extract probability estimates from them.

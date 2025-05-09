import os
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer
import torch.nn.functional as F
from pyprojroot import here
import torch
import numpy as np


class ReasoningModel:
    """
    A model that can be trained to criterion to reason about a causal model with a chain structure.
    The model uses a language model under the hood, which frames the reasoning problem as next-token
    prediction.
    """
    def __init__(
        self,
        model_config={},
        optimizer=None,
        optimizer_args={},
        scheduler=None,
        scheduler_args={},
        pretrained_name=None,
        training_dataset_type="single-sample",
    ):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if pretrained_name is None:
            self.config = GPT2Config(**model_config)
            self.tokenizer = GPT2Tokenizer(
                here("data/tokenizer/vocab.json"), here("data/tokenizer/merges.txt")
            )
            self.model = GPT2LMHeadModel(self.config).to(self.device)
        else:
            model_path = here(os.environ["MODELS_DIR"]) / pretrained_name
            self.model = GPT2LMHeadModel.from_pretrained(model_path).to(self.device)
            self.config = self.model.config
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        if optimizer is not None:
            self.optimizer = optimizer(self.model.parameters(), **optimizer_args)

        if scheduler is not None:
            self.scheduler = scheduler(self.optimizer, **scheduler_args)
        else:
            self.scheduler = None

        self.training_dataset_type = training_dataset_type
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

    def get_next_token_logits(self, prompts):
        """
        Get logits for the next token in the sequence
        """
        tokens = self.tokenizer(prompts, padding=True, return_tensors="pt")[
            "input_ids"
        ].to(self.device)
        outputs = self.model(tokens)
        output_logits = outputs.logits[:, -1, :].squeeze()

        return output_logits

    def read_out_from_layer(self, sequences, layer_num):
        """
        Read out logits by applying the model's language modeling head to the last hidden state of a
        particular layer.
        """
        # tokenize the sequence
        input_ids = self.tokenizer(sequences, return_tensors="pt")["input_ids"].to(
            self.device
        )
        # get the hidden states
        model_output = self.model(input_ids=input_ids, output_hidden_states=True)
        chosen_hidden_state = model_output.hidden_states[layer_num][:, -1, :]
        logits = self.model.lm_head(chosen_hidden_state)

        return logits

    def get_accuracy(self, dataset):
        """
        Get the accuracy in predicting the last token in each sample of the dataset
        """
        sequences, labels = zip(*[(s[:-1], s[-1]) for s in dataset])
        if self.training_dataset_type == "batch-with-separator":
            sequences = ["#\n" + s for s in sequences]

        # get the next-token probabilities
        logits = self.get_next_token_logits(sequences)
        probs = F.softmax(logits, dim=1)
        label_tokens = (
            self.tokenizer(labels, return_tensors="pt")["input_ids"]
            .squeeze()
            .to(self.device)
        )

        # get the probability of the label token
        label_probs = probs[torch.arange(len(label_tokens)), label_tokens]
        return torch.mean(label_probs).item()

    def get_training_batch(self, all_samples, batch_size=16, sample_length=16):
        """
        Get a batch of the training dataset
        """
        if self.training_dataset_type == "single-sample":
            return all_samples
        
        # generate a random batch of samples
        chosen_samples = np.random.choice(all_samples, (batch_size, sample_length), replace=True)

        # add a separator depending on the training dataset type
        if self.training_dataset_type == "batch-no-separator":
            training_strings = ["\n".join(sample) for sample in chosen_samples]
            training_strings = [
                s[4:] if np.random.random() <= 0.5 else s[:-4] for s in training_strings
            ]
        elif self.training_dataset_type == "batch-with-separator":
            training_strings = [
                "#\n" + "\n#\n".join(sample) for sample in chosen_samples
            ]

        return training_strings

    def train_to_criterion(self, train_dataset, threshold: float):
        """
        Train the language model to criterion (defined as the average accuracy exceeding a threshold)
        """
        last_accuracy = 0
        accuracy = 0
        iteration = 0
        # keep training until we hit the threshold
        while accuracy < threshold or last_accuracy < threshold:

            # get the training batch
            batch = self.get_training_batch(train_dataset)

            # encode the dataset
            input_ids = self.tokenizer(batch, return_tensors="pt")["input_ids"].to(
                self.device
            )

            # zero the gradient and make predictions
            self.optimizer.zero_grad()
            output = self.model(input_ids, labels=input_ids)
            loss = output.loss

            # backpropagate the loss
            loss.backward()
            self.optimizer.step()

            # take a step with the learning rate scheduler
            if self.scheduler is not None:
                self.scheduler.step()

            learning_rate = self.optimizer.param_groups[0]["lr"]

            # compute the accuracy
            last_accuracy = accuracy
            accuracy = self.get_accuracy(train_dataset)
            print(
                f"iteration {iteration}: loss={loss.item():.4f}, accuracy={accuracy:.3f}, lr={learning_rate:.6f}"
            )
            iteration += 1

    def save(self, model_name):
        """
        Save the language model and tokenizer to a directory
        """
        save_path = os.environ["MODELS_DIR"] + "/" + model_name
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)

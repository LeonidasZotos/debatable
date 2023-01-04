# Test notebook for semantic sentence comparison.
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import BinaryClassificationEvaluator
from torch.utils.data import DataLoader
from datetime import datetime
import math
import csv
import torch
# Makr sure Cuda cache is clear
torch.cuda.empty_cache()

# Define parameters:
model_name = 'all-mpnet-base-v1'
train_batch_size = 16
num_epochs = 2
model_save_path = 'continuedLearning' + model_name + '-' + datetime.now(
).strftime("%Y-%m-%d_%H-%M-%S")

# Load model

model = SentenceTransformer(
    model_name,
    device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))

# Load data and make train/dev/test split
dataset = 'mrpcDataset'
trainPath = dataset + '/train.csv'
devPath = dataset + '/dev.csv'
testPath = dataset + '/test.csv'

train = []
dev = []
test = []

reader = csv.DictReader(open(trainPath))
for row in reader:
    inp_example = InputExample(texts=[row['sentence1'], row['sentence2']],
                               label=float(row['label']))
    train.append(inp_example)

reader = csv.DictReader(open(devPath))
for row in reader:
    inp_example = InputExample(texts=[row['sentence1'], row['sentence2']],
                               label=float(row['label']))
    dev.append(inp_example)

reader = csv.DictReader(open(testPath))
for row in reader:
    inp_example = InputExample(texts=[row['sentence1'], row['sentence2']],
                               label=float(row['label']))
    test.append(inp_example)

# Setup Train set
trainDataloader = DataLoader(train, batch_size=train_batch_size)
# train_loss = losses.CosineSimilarityLoss(model=model)
train_loss = losses.ContrastiveLoss(model=model)

# Setup Dev set
evaluator = BinaryClassificationEvaluator.from_input_examples(dev,
                                                              name='mrpc-dev')
# evaluator = EmbeddingSimilarityEvaluator.from_input_examples(dev, name='mrpc-dev')

print("fitting model")
# Training the Model
warmup_steps = math.ceil(len(trainDataloader) * num_epochs *
                         0.1)  # 10% of train data for warm-up

model.fit(train_objectives=[(trainDataloader, train_loss)],
          evaluator=evaluator,
          epochs=num_epochs,
          evaluation_steps=10,
          warmup_steps=warmup_steps,
          output_path=model_save_path)

print("evaluating model")

# Store the model and evaluate it
model = SentenceTransformer(
    model_save_path,
    device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))
test_evaluator = BinaryClassificationEvaluator.from_input_examples(
    test, name='mrpc-test')
# test_evaluator = EmbeddingSimilarityEvaluator.from_input_examples(test, name='mrpc-test')
test_evaluator(model, output_path=model_save_path)

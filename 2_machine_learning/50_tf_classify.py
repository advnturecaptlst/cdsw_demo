# # TensorFlow neural network model for multi-class classification

# This example uses one of TensorFlow's 
# [pre-made estimators](https://www.tensorflow.org/guide/estimators#pre-made_estimators).
# Pre-made estimators implement some common machine 
# learning algorithms and enable you to work at a higher 
# level of abstraction than with the base TensorFlow APIs.


# ## Preparation

# Import the required modules
import pandas as pd
import tensorflow as tf

# can use tensorflow for lots of things other than images

# Load data representing one brand of chess set ("set A")
chess = pd.read_csv('data/chess/one_chess_set.csv')

# View the data
chess

# Specify the unique labels (names of the chess pieces)
chess_pieces = ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']

# Split the data into an 80% training set and a 20%
# evaluation (test) set
train = chess.sample(frac=0.8, random_state=42)
test = chess.drop(train.index)

# Separate the features (x) and labels (y) in the 
# training and test datasets
train_x, train_y = train, train.pop('piece')
test_x, test_y = test, test.pop('piece')


# ## TensorFlow setup

# Set constants for TensorFlow
BATCH_SIZE = 100
TRAIN_STEPS = 1000
# TRAIN_STEPS = 10000

# can implement cutoffs to limit training steps if you hit an asymptote

# Define input functions to supply data for training
# and evaulating the model

# The training input function
# 1. Creates a dictionary of features and an array of
#    labels
# 2. Creates a [`tf.data.Dataset`](https://www.tensorflow.org/api_docs/python/tf/data/Dataset)
#    from the two-element tuple `(features, labels)`
# 3. Shuffles, repeats, and batches the `Dataset`, which 
#    controls how TensorFlow iterates over it
# 4. Returns a `tf.data.Dataset` object

# this is referenced under model.train below
def train_input_fn():
  features, labels = dict(train_x), train_y
  dataset = tf.data.Dataset.from_tensor_slices((features, labels))
  dataset = dataset.shuffle(len(train_x)).repeat().batch(BATCH_SIZE)
  return dataset

# deep learning is iterative, if you make your batch size too small it'll take a ton of steps
# and take a long time to train

# The test input function is the same, except it does
# not shuffle or repeat the `Dataset` because that is not
# necessary for evaluation (test) data
def test_input_fn():
  features, labels = dict(test_x), test_y
  dataset = tf.data.Dataset.from_tensor_slices((features, labels))
  dataset = dataset.batch(BATCH_SIZE)
  return dataset


# ## Specifying the model

# Create a list of the feature columns, by calling 
# functions in the 
# [`tf.feature_column`](https://www.tensorflow.org/api_docs/python/tf/feature_column)
# module

# The feature columns in this dataset are all numeric
# columns representing measurements of the chess pieces
# have to use tensorflow specific data types
my_feature_columns = [
  tf.feature_column.numeric_column('base_diameter'),
  tf.feature_column.numeric_column('height'),
  tf.feature_column.numeric_column('weight')
]

# Instantiate an estimator by calling a function in the 
# [`tf.estimator`](https://www.tensorflow.org/api_docs/python/tf/estimator)
# module

# [`DNNClassifier`](https://www.tensorflow.org/api_docs/python/tf/estimator/DNNClassifier)
# is a dense neural network model that can perform
# multi-class classification. It builds feed-forward
# neural networks with all layers fully connected.

# here we specify the structure of the neural net
# as long as you pass a vocabulary for your string outcomes you don't have to convert to int
class_count = len(chess_pieces)

model = tf.estimator.DNNClassifier(
    feature_columns=my_feature_columns,
    hidden_units=[10, 10], # 2 hidden layers with 10 nodes each
    label_vocabulary=chess_pieces,
    n_classes=class_count # len(chess_pieces) could pass a variable rather than a literal
)

# The resulting estimator object (named `model`)
# has methods that can be called to:
# - Train the model
# - Evaluate the trained model
# - Use the trained model to make predictions


# ## Training and evaluating the model

# Call the `train` method to train the model
# iterates 10 times in batches of 100 using gradient descent
model.train(
  input_fn=train_input_fn,
  steps=TRAIN_STEPS
)

# Call the `evaluate` method to evaluate (test) the
# trained model
eval_result = model.evaluate(
  input_fn=test_input_fn
)

# Print the result to examine the accuracy
print(eval_result)


# ## Making predictions

# TF always wants a dictionary of data to pass into
# a function to feed data to predict() 
# See what predictions the model generates for six
# unlabeled chess pieces from "set A" whose features
# are given in this dictionary:
predict_x = {
  'base_diameter': [37.4, 35.9, 32.1, 31, 32.7, 27.3],
  'height': [95.4, 75.6, 46.3, 65.2, 58.1, 45.7],
  'weight': [51, 46, 34, 27, 36, 16]
}

# The predictions we expect the model to make are given
# in this list (but we don't use them to make the 
# predictions):
expected_y = ['King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn']

# Define an input function to supply data for generating
# predictions

# This is similar to the `test_input_fn` function defined
# above, but without labels
def predict_input_fn():
  features = dict(predict_x)
  dataset = tf.data.Dataset.from_tensor_slices(features)
  dataset = dataset.batch(BATCH_SIZE)
  return dataset

# Call the `predict` method to use the trained model to
# make predictions (model persist trained state)
predictions = model.predict(
    input_fn=predict_input_fn
)

# The `predict` method returns a generator that you can
# iterate over to get prediction results for each record.

# code below is only for displaying / printing all predictions
# This loop prints the predictions, their probabilities,
# and the expected predictions:
template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')
for (prediction, expected) in zip(predictions, expected_y):
  class_name = prediction['classes'][0].decode()
  class_id = prediction['class_ids'][0]
  probability = prediction['probabilities'][class_id]
  print(
    template.format(
      class_name,
      100 * probability,
      expected
    )
  )



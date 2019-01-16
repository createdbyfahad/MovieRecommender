import os

from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
from surprise import dump
from surprise import KNNBaseline
from surprise import accuracy
from surprise.model_selection import train_test_split

# Load the movielens-100k dataset (download it if needed),
# data = Dataset.load_builtin('ml-1m')
# file_path = os.path.expanduser('~/Desktop/Project/ml-100k/ratings.csv')
file_path = './api/models/100k/ratings.csv'
# As we're loading a custom dataset, we need to define a reader. In the
# movielens-100k dataset, each line has the following format:
# 'user item rating timestamp', separated by '\t' characters.
reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)

data = Dataset.load_from_file(file_path, reader=reader)
print("Dataset is loaded.")
trainset, testset = train_test_split(data, test_size=.20)
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = KNNBaseline(sim_options=sim_options)
algo.fit(trainset)

# Compute predictions of the 'original' algorithm.
predictions = algo.test(testset)

print("Done training the set.")
accuracy.rmse(predictions, verbose=True)

# Dump algorithm 
# file_name = os.path.expanduser('~/100k_trained_model')
file_path = './api/models/100k/trained_model'
# file_name = os.path.expanduser('~/100k_trained_model')
dump.dump(file_path, algo=algo)

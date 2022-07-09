import sys
from mmEngine.database import load_database
import numpy as np

# Simulate the mean square error or a random model.

num_games = 10000
data = load_database(num_games)

if data is None:
    print(f"Error can't read the database")
    sys.exit(-1)

X, y = data

rng = np.random.default_rng()
random_y = rng.random(y.shape)*2 - 1

mean_squared_error = sum(((y - random_y)**2)/float(y.shape[0]))

print(f"With completely random labels on the first 10000 games have"
        + f" a mean square error of {mean_squared_error}")
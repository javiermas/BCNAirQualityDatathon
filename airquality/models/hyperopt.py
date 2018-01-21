import random
import numpy as np
import pandas as pd

def generate_param_space(iterations, size, dense_units):
    search_space = list() 
    for _ in range(iterations):
        search_space.append({
            'batch_size': random.choice(range(100)),
            'seq_length': 1,
            'size': size,
            'hidden_units': random.choice(range(20, 200)),
            'num_layers': 1,
            'dense_units': dense_units,
            'dropout': random.choice(np.linspace(0, 1, 100)),
            'epochs': random.choice(range(30, 150)),
            'epochs_after': random.choice(range(5, 30)),
            'learning_rate': random.choice(np.linspace(0.0001, 0.1, 100)),
            'log_loss': np.nan,
            'mse': np.nan,
        })

    search_space = pd.DataFrame.from_dict(search_space, orient='columns')
    return search_space

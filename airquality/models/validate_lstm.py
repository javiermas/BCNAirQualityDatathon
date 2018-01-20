from airquality.data.read_data import read_obs, read_targets
from airquality.models.LSTM_keras import LSTM_K
from airquality.data.prepare_data import create_model_matrix
from airquality.models.split import tt_split, reshape_to_keras

# Read data
data_obs = read_obs(path='/home/yc00032/Desktop/Just_Peanuts_II/BCNAirQualityDatathon/data/processed/all_obs.csv')
data_targets = read_targets(path='/home/yc00032/Desktop/Just_Peanuts_II/BCNAirQualityDatathon/data/processed/targets.csv')
target_cols = data_targets.drop(columns=['date']).columns

# Prepare data
seq_length = 1
model_matrix = create_model_matrix(data_obs, target_cols=list(target_cols))
train_size = int(len(model_matrix)*0.7)
train_X, test_X, train_Y, test_Y = tt_split(model_matrix, train_size, target_cols)
train_X = reshape_to_keras(train_X, seq_length)
test_X = reshape_to_keras(test_X, seq_length)

# Validate LSTM
param_dict = {
    'batch_size': 10,
    'seq_length': seq_length,
    'size': train_X.shape[2],
    'hidden_units': 50,
    'num_layers': 1,
    'dense_units': train_Y.shape[1],
    'epochs': 3,
}

lstm = LSTM_K(**param_dict)
lstm.validate(train_X, train_Y, test_X, test_Y)

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from airquality.data.read_data import read_obs, read_targets
from airquality.models.LSTM_keras import LSTM_K
from airquality.data.prepare_data import create_model_matrix, sequences_to_columns
from airquality.models.split import tt_split, reshape_to_keras
from airquality.models.hyperopt import generate_param_space

# Read data
data_roll_path = '/Users/b.yc0006/Cloud/BCNAirQualityDatathon/data/processed/data_roll_day_dist.csv'
data = pd.read_csv(data_roll_path)
data['date'] = pd.to_datetime(data['date'])

# Prepare data
stations = data['station'].unique()
target_cols = ['conc_obs'+'_'+station for station in stations]
cols = [
    'date',
    'station',
    'conc_model_1',
    'conc_model_2',
    'conc_obs_lag1',
    'target_lag1',
    'conc_obs',
    'LastT',
    'season',
    'week_day',
    'yhat_lower',
    'yhat_upper',
]
cols_l = [col for col in cols if col not in ['date', 'station']]
for col in cols_l:
    data.loc[data[col] < 0, col] = np.nan

data = data[cols].sort_values(['date', 'station']).reset_index(drop=True).ffill()
data = data.fillna(0)
scaler = MinMaxScaler(feature_range=(0, 1))
for col in cols_l:
    data[col] = scaler.fit_transform(data[col].values.reshape([-1,1]))

model_matrix = sequences_to_columns(data, cols).drop('date', axis=1) #730

# Tune
seq_length = 1
train_size = 15 
test_size = 730-15
train_X, test_X, eval_X, train_Y, test_Y, eval_Y = tt_split(model_matrix, train_size, test_size, target_cols)
train_X = reshape_to_keras(train_X, seq_length)
test_X = reshape_to_keras(test_X, seq_length)
eval_X = reshape_to_keras(eval_X, seq_length)
print('Shapes')
print('train X: (%d, %d, %d)' % train_X.shape)
print('test X: (%d, %d, %d)' % test_X.shape)
print('train Y: (%d, %d)' % train_Y.shape)
print('test Y: (%d, %d)' % test_Y.shape)
print('eval X: (%d, %d, %d)' % eval_X.shape)
print('eval Y: (%d, %d)' % eval_Y.shape)

d = {
    'batch_size': 57,
    'seq_length': 1,
    'size': train_X.shape[2],
    'hidden_units': 50,
    'num_layers': 1,
    'dense_units': train_Y.shape[1],
    'dropout': 0.04,
    'epochs': 60,
    'epochs_after': 15,
    'learning_rate': 0.03,
}

lstm = LSTM_K(**d)
lstm.validate(train_X, train_Y, test_X, test_Y, scaler)
predictions = lstm.predict(eval_X, scaler)
eval_Y = eval_Y.reshape([-1, 1])
eval_Y = scaler.inverse_transform(eval_Y)
eval_Y = eval_Y.reshape([-1, d['dense_units']])

padded = np.zeros((train_size, d['dense_units']))
train_set = np.vstack((padded, np.vstack((lstm.predictions_cum))))
predictions_LSTM = np.vstack((train_set, eval_Y))

for s in range(7):
    plt.plot(predictions_LSTM[:, s], label='prediction')
    plt.plot(model_matrix[cols].iloc[:, s], label='label')
    plt.legend()
    plt.savefig('../../reports/predictions/final_prediction'+str(s)+'.pdf')
    plt.close()

pd.DataFrame(eval_Y, columns=data['station'].unique()).to_csv('../../data/processed/predictions_LSTM.csv')

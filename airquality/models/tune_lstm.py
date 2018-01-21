import pandas as pd
from matplotlib import pyplot as plt
from airquality.data.read_data import read_obs, read_targets
from airquality.models.LSTM_keras import LSTM_K
from airquality.data.prepare_data import create_model_matrix, sequences_to_columns
from airquality.models.split import tt_split, reshape_to_keras
from airquality.models.hyperopt import generate_param_space

# Read data

data_roll_path = '/home/yc00032/Desktop/Just_Peanuts_II/BCNAirQualityDatathon/data/data_roll_day.csv'
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
]
data = data[cols].sort_values(['date', 'station']).reset_index(drop=True)
model_matrix = sequences_to_columns(data, cols).drop('date', axis=1)[:725] #725

# Tune
seq_length = 1
train_size = int(len(model_matrix)*0.7)
train_X, test_X, train_Y, test_Y = tt_split(model_matrix, train_size, target_cols)
train_X = reshape_to_keras(train_X, seq_length)
test_X = reshape_to_keras(test_X, seq_length)
print('Shapes')
print('train X: (%d, %d, %d)' % train_X.shape)
print('test X: (%d, %d, %d)' % test_X.shape)
print('train Y: (%d, %d)' % train_Y.shape)
print('test Y: (%d, %d)' % test_Y.shape)

n_iterations = 100 
param_df = generate_param_space(n_iterations, train_X.shape[2], train_Y.shape[1])
param_dict = param_df.to_dict(orient='records')
i = 0
for d in param_dict:
    int_cols = [col for col in list(param_df.columns)\
        if col not in ['learning_rate', 'log_loss', 'mse', 'dropout']]
    for key in int_cols: 
        d[key] = int(d[key])

    d.pop('log_loss')
    d.pop('mse')
    lstm = LSTM_K(**d)
    mse, log_loss = lstm.validate(train_X, train_Y, test_X, test_Y)
    print(d)
    print('MSE:', mse, 'Log loss:', log_loss)
    param_df.loc[i, 'mse'] = mse
    param_df.loc[i, 'log_loss'] = log_loss
    param_df.to_pickle('../../reports/param_df'+str(i)+'.p')
    for s in range(7):
        plt.plot(lstm.predictions_cum[:,s], label='prediction')
        plt.plot(test_Y[:,s], label='label')
        plt.legend()
        plt.savefig('../../reports/predictions/predic'+str(s)+str(i)+'.pdf')
        plt.close()

    i += 1

print(param_df)



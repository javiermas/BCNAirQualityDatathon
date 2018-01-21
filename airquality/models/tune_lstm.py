from airquality.data.read_data import read_obs, read_targets
from airquality.models.LSTM_keras import LSTM_K
from airquality.data.prepare_data import create_model_matrix
from airquality.models.split import tt_split, reshape_to_keras
from airquality.models.hyperopt import generate_param_space

# Read data
data_obs = read_obs()
data_targets = read_targets()
target_cols = data_targets.columns[:-1]

# Prepare data
seq_length = 1
model_matrix = create_model_matrix(data_obs, target_cols=list(target_cols))[:50]
train_size = int(len(model_matrix)*0.7)
train_X, test_X, train_Y, test_Y = tt_split(model_matrix, train_size, target_cols)
train_X = reshape_to_keras(train_X, seq_length)
test_X = reshape_to_keras(test_X, seq_length)

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
    print d
    print 'MSE:', mse, 'Log loss:', log_loss
    param_df.loc[i, 'mse'] = mse
    param_df.loc[i, 'log_loss'] = log_loss
    param_df.to_pickle('../../reports/param_df'+str(i)+'.p')
    i += 1

print param_df



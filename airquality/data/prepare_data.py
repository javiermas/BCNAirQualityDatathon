import pandas as pd


def create_model_matrix(features, target, lags):
    features = create_lagged_features(pd.concat([features, target], axis=1), lags)
    model_matrix = pd.concat([features, target], axis=1)
    return model_matrix


def create_lagged_features(data, lags):
    '''This function takes a time series and
    returns a dataframe with <lags> 
    1-to-lag lagged features.'''
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    
    data_list = []
    for lag in range(lags+1):
        shifted_data = data.shift(lag)
        colnames = [col+'_lag_'+str(lag) for col in data.columns]
        shifted_data.columns = colnames
        data_list.append(shifted_data)
    
    data = pd.concat(data_list, axis=1).dropna()
    return data

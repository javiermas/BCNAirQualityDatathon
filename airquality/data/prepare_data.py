import pandas as pd


def create_model_matrix(features=None, target=None, lags=1):
    '''Pass features and target as dataframes.'''
    if features is None:
        lagged_target = create_lagged_features(target, lags)
        model_matrix = pd.concat([target, lagged_target], axis=1).dropna()
        return model_matrix

    features = create_lagged_features(pd.concat([features, target], axis=1), lags)
    model_matrix = pd.concat([features, target], axis=1).dropna()
    return model_matrix


def create_lagged_features(data, lags):
    '''This function takes a time series and
    returns a dataframe with <lags> 
    1-to-lag lagged features.'''
    data_list = []
    for lag in range(1, lags+1):
        shifted_data = data.shift(lag)
        col_dict = {}
        for col in data.columns:
            col_dict[col] = col+'_lag_'+str(lag)

        shifted_data = shifted_data.rename(columns=col_dict)
        data_list.append(shifted_data)
    
    data = pd.concat(data_list, axis=1)
    return data

def create_ts_df(all_models_data):
    new_data = pd.DataFrame()
    for station in data['station'].unique():
	new_data[station] = data.loc[data['station'] == station, 
		'Concentration'].reset_index(drop=True)
    
    return new_data


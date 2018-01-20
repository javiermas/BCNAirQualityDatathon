import pandas as pd
import datetime
from geopy.distance import vincenty


def create_model_matrix(features=None, target=None, lags=1):
    '''Pass features and target as dataframes.'''
    if features is None:
        lagged_target = create_lagged_features(target, lags)
        model_matrix = pd.concat([target, lagged_target], axis=1).dropna()
        return model_matrix

    features = create_lagged_features(pd.concat([features, target], axis=1),
                                      lags)
    model_matrix = pd.concat([features, target], axis=1).dropna()
    return model_matrix


def create_lagged_features(data, lags):
    '''
    This function takes a time series and
    returns a dataframe with <lags>
    1-to-lag lagged features.
    '''
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


def create_ts_df(data):
    new_data = pd.DataFrame()
    for station in data['station'].unique():
        new_data[station] = data.loc[
            data['station'] == station, 'Concentration'
        ].reset_index(drop=True)

    return new_data



def gen_daily_targets(data):
    data = data\
        .groupby(by=['day', 'station'])['Concentration']\
        .max().reset_index()
    data['target'] = 0
    data.loc[data['Concentration'] > 100, 'target'] = 1

    # data.to_csv('data/daily_targets.csv')
    return data


def _add_holidays(data, row):
    data.loc[(data['day'] == row['day']) &
             (data['month'] == row['month']) &
             (data['year'] == row['year']), 'holiday'] = 1


def gen_date_features(data):
    dies = [1, 29, 1, 1, 20, 24, 15, 11, 24, 12, 1, 6, 25, 26,
            1, 6, 18, 21, 1, 9, 24, 15, 11, 24, 1, 6, 8, 25, 26,
            1, 6, 3, 6, 1, 1, 24, 15, 11, 24, 12, 8, 25, 26]
    mes = [1, 3, 4, 5, 5, 6, 8, 9, 9, 10, 11, 12, 12, 12,
           1, 1, 4, 4, 5, 6, 6, 8, 9, 9, 11, 12, 12, 12, 12,
           1, 1, 4, 4, 5, 6, 6, 8, 9, 9, 10, 12, 12, 12]

    anys = [2013] * 14 + [2014] * 15 + [2015] * 14

    holidays = pd.DataFrame({'day': dies, 'month': mes, 'year': anys})

    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['week_day'] = data['date'].dt.dayofweek
    data['day'] = data['date'].dt.day
    data['weekend'] = 0
    data.loc[data['week_day'] > 4, 'weekend'] = 1
    data['holiday'] = 0
    holidays.apply(lambda row: _add_holidays(data, row), axis=1)
    data.loc[data['week_day'] > 4, 'holiday'] = 1

    for year in [2013, 2014, 2015]:
        data.loc[(data['date'] >= datetime.date(year - 1, 12, 21)) &
                 (data['date'] <= datetime.date(year, 3, 20)), 'season'] = 0
        data.loc[(data['date'] >= datetime.date(year, 3, 21)) &
                 (data['date'] <= datetime.date(year, 6, 20)), 'season'] = 1
        data.loc[(data['date'] >= datetime.date(year, 6, 21)) &
                 (data['date'] <= datetime.date(year, 9, 20)), 'season'] = 2
        data.loc[(data['date'] >= datetime.date(year, 9, 21)) &
                 (data['date'] <= datetime.date(year, 12, 20)), 'season'] = 3
        data.loc[(data['date'] >= datetime.date(year, 12, 21)) &
                 (data['date'] <= datetime.date(year + 1, 3, 20)), 'season'] = 0

    return data


def gen_distances(stations):
    stations = stations.rename(columns={'code': 'station'})
    for st in stations['station']:
        stations['dist_to_' + st] = 0
        for i in stations.index:
            dist = vincenty((stations.loc[i, 'lat'], stations.loc[i, 'lon']),
                            (stations[stations['station'] == st]['lat'].iloc[0],
                             stations[stations['station'] == st]['lon'].iloc[0]))
            stations.loc[i, 'dist_to_' + st] = dist.km

    return stations

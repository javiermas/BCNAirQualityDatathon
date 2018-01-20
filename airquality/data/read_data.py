import pandas as pd
from airquality.data.prepare_data import create_ts_df


def read_obs(path='/Users/b.yc0006/Cloud/BCNAirQualityDatathon/data/processed/all_obs.csv'):
    data = pd.read_csv(path).rename(columns={
         'AirQualityStationEoICode': 'station',
         'DatetimeBegin': 'datetime',
         'Concentration': 'concentration'
    })

    data['datetime'] = pd.to_datetime(data['datetime'])
    data = data.sort_values(['station', 'datetime']).reset_index(drop=True)
    data = create_ts_df(data, 'datetime')
    data['date'] = data['datetime'].dt.date
    return data


def read_targets(path='/Users/b.yc0006/Cloud/BCNAirQualityDatathon/data/raw/targets.csv'):
    target = pd.read_csv(path).rename(columns={
        'target': 'concentration',
    })
    target['date'] = pd.to_datetime(target['date'])
    target = target.sort_values(['station', 'date']).reset_index(drop=True)
    target = create_ts_df(target, 'date')
    return target

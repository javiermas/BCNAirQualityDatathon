import pandas as pd

def gen_daily_targets(df_obs)

    daily_targets = df_obs.groupby(by=['day', 'AirQualityStation'])['Concentration'].max().reset_index()
    daily_targets['target'] = 0
    daily_targets.loc[daily_targets['Concentration'] > 100, 'target'] = 1

    # daily_targets.to_csv('data/daily_targets.csv')
    return daily_targets

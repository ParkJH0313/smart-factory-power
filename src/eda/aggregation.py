"""
Data Aggregation Functions for EDA
5초 데이터를 시간 단위로 집계
"""

import pandas as pd
import numpy as np

def aggregate_to_hourly(df, target_col='activePower'):
    """5초 데이터를 1시간 단위로 집계"""
    
    # activePower는 통계 전부
    power_agg = df.set_index('datetime')[target_col].resample('1h').agg([
        'mean', 'std', 'min', 'max', 'count'
    ])
    power_agg.columns = [f'{target_col}_{stat}' for stat in power_agg.columns]
    
    # 나머지 변수는 평균만
    other_cols = [
        'voltageR', 'voltageS', 'voltageT',
        'voltageRS', 'voltageST', 'voltageTR',
        'currentR', 'currentS', 'currentT',
        'powerFactorR', 'powerFactorS', 'powerFactorT',
        'reactivePowerLagging', 'operation'
    ]
    
    other_agg = df.set_index('datetime')[other_cols].resample('1h').mean()
    
    # 합치기
    df_hourly = pd.concat([power_agg, other_agg], axis=1).reset_index()
    
    # 시간 Feature 추가
    df_hourly['hour'] = df_hourly['datetime'].dt.hour
    df_hourly['day'] = df_hourly['datetime'].dt.day
    df_hourly['month'] = df_hourly['datetime'].dt.month
    df_hourly['weekday'] = df_hourly['datetime'].dt.dayofweek
    df_hourly['is_weekend'] = (df_hourly['weekday'] >= 5).astype(int)
    
    return df_hourly
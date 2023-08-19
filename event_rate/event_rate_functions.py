import glob
import pandas as pd

def read_and_concat_data(path):
    dfs = list(map(pd.read_hdf, glob.glob(path + '/*/*hdf')))
    return pd.concat(dfs, verify_integrity=True)

def data_selection(df):
    return df[(df.is_pulser        == False) & 
              (df.is_baseline      == False) & 
              (df.is_muon_tagged   == False) & 
              (df.is_valid_channel == True ) & 
              (df.multiplicity     == 1    ) &
              (df.is_physical      == True )]

def resample_df(df, timestamp='H'): ## returns the event rates in mHz (evt rate per hour /3600 sec *1000 mHz)
    event_rate_df        = df.resample(timestamp).size()
    event_rate_df_series = pd.Series(event_rate_df.values*(1000/3600), index=event_rate_df.index)
    return event_rate_df_series

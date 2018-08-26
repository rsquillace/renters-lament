import pandas as pd
import numpy as np

def transform_rent(rent_df):
    rent_df['zipcode'] = rent_df['zipcode'].astype(str).str.cat(rent_df['neighborhood'], sep=': ')
    rent_df = rent_df.drop(columns=['neighborhood'])
    transposed = rent_df.set_index('zipcode').T.reset_index().copy()
    transposed = transposed.rename(columns={'index':'year'})
    transposed['year'] = transposed['year'].astype(int)
    return transposed

def merge_rent_wage(rent_df, wage_df):
    rent_trans = transform_rent(rent_df)
    merged =  pd.merge(wage_df, rent_trans, on='year', how='left')
    for col in merged.loc[:, merged.columns.str.startswith('98')].columns:
        merged[col] = merged[col] <= merged['monthly_rent_allowance']
    return merged

def retrieve_affordable_zips(rent_df, wage_df, industry_name, year):
    merged = merge_rent_wage(rent_df, wage_df)
    aff = merged.loc[:, merged.columns.str.startswith('98')].loc[(merged['industry'] == industry_name)&(merged['year'] == year)].values[0]
    zips = merged.loc[:, merged.columns.str.startswith('98')].columns
    return zips[aff]

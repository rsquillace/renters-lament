import pandas as pd
import numpy as np

def transform_rent(rent_df):
    trans_rent = []
    for year in range(2011,2018):
        year_df = rent_df[rent_df['year']==year].filter(items=['zipcode', 'med_rent']).copy()
        transposed = year_df.astype(int).T.reset_index(drop=True).copy()
        transposed.columns = transposed.iloc[0].astype(str)
        transposed = transposed.drop([0])
        transposed['year'] = year
        trans_rent.append(transposed)
    return pd.concat(trans_rent)

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

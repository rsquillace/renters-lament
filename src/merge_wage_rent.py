import pandas as pd
import numpy as np

def transform_rent(rent_df):
    trans_rent = pd.melt(rent_df, id_vars=["zipcode", "neighborhood"], var_name="year", value_name="med_rent").copy()
    trans_rent['year'] = trans_rent['year'].astype(int)
    return trans_rent

def merge(rent_df, wage_df):
    rent_trans = transform_rent(rent_df)
    merged =  pd.merge(wage_df, rent_trans, on='year', how='left')
    merged['affordable'] = merged ['med_rent'] <= merged['monthly_rent_allowance']
    merged['zipcode'] = merged['zipcode'].astype(str)
    return merged

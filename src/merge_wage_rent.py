import pandas as pd
import numpy as np

def transform_rent(rent_df):
    transformed_rent = pd.melt(rent_df, id_vars=["zipcode", "neighborhood"], var_name="year", value_name="med_rent").copy()
    transformed_rent['year'] = transformed_rent['year'].astype(int)
    return transformed_rent

def merge(one_bed_rent_df, two_bed_rent_df, wage_df):
    one_bed_rent = transform_rent(one_bed_rent_df)
    two_bed_rent = transform_rent(two_bed_rent_df)
    one_bed_merge = pd.merge(wage_df, one_bed_rent, on='year', how='left')
    one_bed_merge['bedrooms'] = 1
    one_bed_merge['affordable'] = one_bed_merge['med_rent'] <= one_bed_merge['monthly_rent_allowance']
    two_bed_merge = pd.merge(wage_df, two_bed_rent, on='year', how='left')
    two_bed_merge['bedrooms'] = 2
    two_bed_merge['affordable'] = (two_bed_merge['med_rent'] / 2) <= two_bed_merge['monthly_rent_allowance']
    merged = pd.concat([one_bed_merge, two_bed_merge]).reset_index(drop=True)
    merged['zipcode'] = merged['zipcode'].astype(str)
    return two_bed_merge

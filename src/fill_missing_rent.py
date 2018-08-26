import pandas as pd
import numpy as np

def make_rolling_mean_column(sale_df):
    rolling_df = []
    for zc in sale_df['zipcode'].unique():
        zip_df = sale_df[sale_df['zipcode'] == zc].copy()
        zip_df['rolling_mean'] = zip_df['med_sale_price'].rolling(2, min_periods=1).median()
        rolling_df.append(zip_df)
    return pd.concat([*rolling_df])

def make_normalized_dic(sale_df, rent_df, zipcode):
    sales = make_rolling_mean_column(sale_df)
    sale_zip = sales[sales['zipcode'] == zipcode].copy()
    non_null = rent_df.columns[rent_df[rent_df['zipcode'] == zipcode].notnull().any()].tolist()
    earliest_known_year = min(non_null)
    sale_zip['norm'] = sale_zip['rolling_mean'] / sale_zip[sale_zip['year'] == int(earliest_known_year)]['rolling_mean'].item()
    dic = {}
    for year in sale_zip['year'].unique():
        dic[str(year)] = sale_zip[sale_zip['year'] == year]['norm'].item()
    for k,v in dic.items():
        dic[k] = v * rent_df[rent_df['zipcode'] == zipcode][earliest_known_year].item()
    return dic

def fill_rent(sale_df, rent_df):
    for zc in rent_df['zipcode'].unique():
        norm_dic = make_normalized_dic(sale_df, rent_df, zc)
        null = rent_df.columns[rent_df.isnull().any()].tolist()
        for year in null:
            rent_df.at[rent_df['zipcode'] == zc, year] = norm_dic[year]
    return rent_df

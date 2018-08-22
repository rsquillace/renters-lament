import pandas as pd
import numpy as np

def create_normalization_dic(sale_df, year):
    year_sales = sale_df[sale_df['year'] == year].copy()
    normalized_dic = {}
    zipcodes = sale_df['zipcode'].unique()
    for zc in zipcodes:
         normalized_dic[zc] = year_sales['med_sale_price'][year_sales['zipcode'] == zc].item()/year_sales['med_sale_price'][year_sales['zipcode']==98122].item()
    return normalized_dic

def fill_in_values(rent_df, sale_df):
    filled_in_dfs = []
    for year in range(2011,2018):
        year_rent = rent_df[rent_df['year'] == year].copy()
        normalized_dic = create_normalization_dic(sale_df, year)
        rent98122 = year_rent['med_rent'][year_rent['zipcode']==98122].item()
        est_rent = {}
        for k,v in normalized_dic.items():
            est_rent[k] = v * rent98122
        year_rent['med_rent'] = year_rent['med_rent'].fillna(year_rent['zipcode'].map(est_rent))
        filled_in_dfs.append(year_rent)
    return pd.concat(filled_in_dfs)

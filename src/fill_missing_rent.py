import pandas as pd
import numpy as np


def make_rolling_mean_column(sale_df):

    '''
    Creates a new dataframe for sales using the rolling mean of sales trends

    INPUT: Sales dataframe
    OUTPUT: Sales dataframe with rolling means
    '''

    rolling_df = []
    for zc in sale_df['zipcode'].unique():
        zip_df = sale_df[sale_df['zipcode'] == zc].copy()
        zip_df['rolling_mean'] = zip_df['med_sale_price'].rolling(2, min_periods=1).median()
        rolling_df.append(zip_df)
    return pd.concat([*rolling_df])


def make_normalized_dic(sale_df, rent_df, zipcode):

    '''
    Makes a dictionary of missing years and their extrapolated rents for the specified zip code. Found by normalizing sale prices by the median sale price for the year associated with the earliest known rent. It then scales values by the known rent

    INPUT: Sales dataframe, rent dataframe, zip code of interest
    OUTPUT: Dictionary with each missing year and the extrapolated rent value for that year
    '''

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

    '''
    Fills rent dataframe with values of missing years

    INPUT: Sales dataframe, rent dataframe
    OUTPUT: Rent dataframe with values for all years filled in
    '''

    for zc in rent_df['zipcode'].unique():
        norm_dic = make_normalized_dic(sale_df, rent_df, zc)
        null = rent_df.columns[rent_df[rent_df['zipcode'] == zc].isnull().any()].tolist()
        for year in null:
            rent_df.at[rent_df['zipcode'] == zc, year] = norm_dic[year]
    return rent_df

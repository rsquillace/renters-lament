import pandas as pd
import numpy as np


'''
Zip code list self compiled, using a list of Seattle zip codes and weeding out areas not of interest
'''

seattle_zips =[98101, 98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109, 98112, 98115, 98116, 98117, 98118, 98119, 98121, 98122, 98125, 98126, 98133, 98136, 98144, 98177, 98199]


'''
Public sale records are not released with an attached address. To find the address of each sale, building info must be joined with the sales dataframe
'''


def clean_sale_data(sale_filepath):

    '''
    Retrieves sale records occuring in the years of interest

    INPUT: Filepath to public sale records
    OUTPUT: Dataframe of all sales occuring in the desired locations and timeframe
    '''

    sale_data = pd.read_csv(sale_filepath)
    pruned_sales = sale_data.filter(items=['Major','Minor', 'DocumentDate', 'SalePrice']).copy()
    pruned_sales['year'] = pd.to_datetime(pruned_sales['DocumentDate'], format='%m/%d/%Y').dt.year
    pruned_sales = pruned_sales[pruned_sales['SalePrice'] != 0].reset_index(drop=True)
    pruned_sales[['Major','Minor']] = pruned_sales[['Major','Minor']].astype(int)
    clean_sales = pruned_sales.filter(items=['Major','Minor','year','SalePrice']).copy()
    clean_sales = clean_sales[clean_sales['year'].isin(range(2011,2018))].copy()
    return clean_sales


def clean_residential_data(res_filepath):

    '''
    Retrieves information for residential buildings in desired zipcodes with 1-4 bedrooms

    INPUT: Filepath to residential building records
    OUTPUT: Dataframe containing residential building info
    '''

    residential_data = pd.read_csv(res_filepath)
    pruned_res = residential_data[residential_data['Bedrooms'].isin([1,2,3,4])].reset_index(drop=True).copy()
    pruned_res = pruned_res[pruned_res['ZipCode'].isin(seattle_zips)].reset_index(drop=True)
    clean_res = pruned_res.filter(items=['Major','Minor','ZipCode']).copy()
    return clean_res


def clean_condo_data(condo_filepath):

    '''
    Retrieves information for condos in desired zipcodes with 1-4 bedrooms

    INPUT: Filepath to condo records
    OUTPUT: Dataframe containing condo info
    '''

    condo_data = pd.read_csv(condo_filepath)
    reduced_condo = condo_data[(condo_data['UnitType'].isin([1,2]))&(condo_data['NbrBedrooms'].isin(['1','2','3','4']))].copy()
    pruned_condo = reduced_condo.filter(items=['Major','Minor','ZipCode']).dropna().copy()
    pruned_condo = pruned_condo[pruned_condo['ZipCode'] != ' ']
    pruned_condo = pruned_condo.replace('98107-3018','98107')
    pruned_condo['ZipCode'] = pruned_condo['ZipCode'].astype(int)
    clean_condo = pruned_condo[pruned_condo['ZipCode'].isin(seattle_zips)].copy()
    return clean_condo


def aggregate_dataframes(sale_filepath, res_filepath, condo_filepath):

    '''
    Joins sale info with the associated residence being sold

    INPUT: Filepath to sale records, filepath to residential records, filepath to condo records
    OUTPUT: Dataframe containing all sales for desired zip codes in the specified timeframe
    '''

    sale_df = clean_sale_data(sale_filepath)
    res_df = clean_residential_data(res_filepath)
    cond_df = clean_condo_data(condo_filepath)
    res_sale = pd.merge(res_df,sale_df, on=['Major','Minor'], how='inner')
    cond_sale = pd.merge(cond_df,sale_df, on=['Major','Minor'], how='inner')
    all_sales = pd.concat([res_sale, cond_sale], sort=False).reset_index(drop=True)
    clean_sales = all_sales.filter(items=['year','SalePrice','ZipCode']).copy()
    clean_sales = clean_sales.rename(columns={'ZipCode':'zipcode','SalePrice':'med_sale_price'})
    grouped_clean_sales = clean_sales.groupby(['year', 'zipcode']).median().reset_index()
    return grouped_clean_sales

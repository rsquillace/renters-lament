import pandas as pd
import numpy as np

seattle_zips = [98103, 98115, 98133, 98122, 98125, 98109, 98105, 98118, 98102, 98107, 98117, 98121, 98116, 98112, 98101, 98126, 98104]

def clean_sale_data(sale_filepath):
    sale_data = pd.read_csv(sale_filepath)
    pruned_sales = sale_data.filter(items=['Major','Minor', 'DocumentDate', 'SalePrice']).copy()
    pruned_sales['year'] = pd.to_datetime(pruned_sales['DocumentDate'], format='%m/%d/%Y').dt.year
    pruned_sales = pruned_sales[pruned_sales['SalePrice'] != 0].reset_index(drop=True)
    pruned_sales[['Major','Minor']] = pruned_sales[['Major','Minor']].astype(int)
    clean_sales = pruned_sales.filter(items=['Major','Minor','year','SalePrice']).copy()
    clean_sales = clean_sales[clean_sales['year'].isin(range(2011,2018))].copy()
    return clean_sales

def clean_residential_data(res_filepath):
    residential_data = pd.read_csv(res_filepath)
    pruned_res = residential_data[residential_data['Bedrooms'].isin([1,2,3,4])].reset_index(drop=True).copy()
    pruned_res = pruned_res[pruned_res['ZipCode'].isin(seattle_zips)].reset_index(drop=True)
    clean_res = pruned_res.filter(items=['Major','Minor','ZipCode']).copy()
    return clean_res

def clean_condo_data(condo_filepath):
    condo_data = pd.read_csv(condo_filepath)
    reduced_condo = condo_data[(condo_data['UnitType'].isin([1,2]))&(condo_data['NbrBedrooms'].isin(['1','2','3','4']))].copy()
    pruned_condo = reduced_condo.filter(items=['Major','Minor','ZipCode']).dropna().copy()
    pruned_condo = pruned_condo[pruned_condo['ZipCode'] != ' ']
    pruned_condo = pruned_condo.replace('98107-3018','98107')
    pruned_condo['ZipCode'] = pruned_condo['ZipCode'].astype(int)
    clean_condo = pruned_condo[pruned_condo['ZipCode'].isin(seattle_zips)].copy()
    return clean_condo

def aggregate_dataframes(sale_filepath, res_filepath, condo_filepath):
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

import pandas as pd
import numpy as np

'''
Zip code list self compiled, using a list of Seattle zip codes and weeding out areas not of interest
'''

seattle_zipcodes =  [98101, 98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109, 98112, 98115, 98116, 98117, 98118, 98119, 98121, 98122, 98125, 98126, 98133, 98136, 98144, 98177, 98199]


def clean_rental_data(rent_filepath):

    '''
    Retrieves rental data for zip codes of interest, groups them by year and takes median rent

    INPUT: Filepath to zip code rental data
    OUTPUT: Dataframe containing rental data for zipcodes of interest for available years
    '''

    rent_data = pd.read_csv(rent_filepath)
    reduced_rent = rent_data[rent_data['RegionName'].isin(seattle_zipcodes)].copy()
    pruned_rent = reduced_rent.dropna(axis=1, how='all').copy()
    years=[]
    for num in range(2011,2018):
        years.append(str(num))
    for year in years:
        pruned_rent[year] = pruned_rent.loc[:, pruned_rent.columns.str.startswith(year)].median(axis=1)
    pruned_rent = pruned_rent.rename(columns={'RegionName':'zipcode'})
    clean_rent = pruned_rent.filter(items=['zipcode', *years]).reset_index(drop=True).copy()
    return clean_rent

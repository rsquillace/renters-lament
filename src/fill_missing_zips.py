import pandas as pd
import numpy as np

'''
Neighborhoods named manually based on personal familiarity and knowledge of neigborhood location in Seattle
'''

neighborhoods = {98101: 'Downtown', 98102: 'Captiol Hill', 98103: 'Wallingford', 98104: 'Pioneer Square', 98105: 'University District', 98106: 'Highland Park', 98107: 'Ballard', 98108: 'Georgetown/Beacon Hill', 98109: 'Westlake', 98112: 'Montlake', 98115 : 'Wedgewood', 98116: 'West Seattle/Alki', 98117: 'Crown Hill', 98118: 'Rainier Valley', 98119: 'Queen Anne', 98121: 'BellTown', 98122: 'Capitol Hill/Madrona', 98125: 'Lake City', 98126: 'West Seattle', 98133: 'North Park', 98136: 'Fauntleroy', 98144: 'Mt. Baker', 98177: 'Richmond Beach', 98199: 'Magnolia'}


'''
Surrounding zip codes compiled manually by looking at map for the missing zip codes of interest and chosing the zip code with the greatest shared boundary that had rental info for 2017. Note different zip codes missing for one and two bedroom rental data
'''

one_surrounding = {98106: 98126, 98108: 98118, 98119: 98109, 98136: 98116, 98144: 98122, 98177:98117, 98199:98107}

two_surrounding = {98108: 98118, 98109:98102, 98119:98199, 98121: 98101, 98136: 98116, 98177: 98117}


def fill_missing_zips(room_rent_df, sale_df, surrounding_dic):

    '''
    Fills in 2017 rent for missing zip codes. Does so using ratio of sale prices to surrounding zip codes and scaling by the known rent

    INPUT: Cleaned rent dataframe, cleaned sale dataframe, dictionary of surrounding zip codes
    OUTPUT: Rent dataframe with all zip codes of interest
    '''

    s2017 = sale_df[sale_df['year'] == 2017].copy()
    ratio = {}
    for k,v in surrounding_dic.items():
        ratio[k] = [v,s2017[s2017['zipcode'] == k]['med_sale_price'].item()/s2017[s2017['zipcode'] == v]['med_sale_price'].item()]
    r2017 = room_rent_df.filter(items = ['zipcode', '2017'])
    fill_in = {}
    for k,v in ratio.items():
        fill_in[k] = r2017[r2017['zipcode'] == v[0]]['2017'].item()*v[1]
    for k, v in fill_in.items():
         room_rent_df = room_rent_df.append({'zipcode': k, '2017': v}, ignore_index=True)
    years = []
    for num in range(2011,2018):
        years.append(str(num))
    room_rent_df['neighborhood'] = room_rent_df['zipcode'].map(neighborhoods)
    added_zips = room_rent_df.filter(items=['zipcode', 'neighborhood', *years]).reset_index(drop=True).copy()
    return added_zips


def apply_to_one_bed(one_bed_rent_df, sale_df):

    '''
    Fills in missing one bedroom zipcodes

    INPUT: One bedroom rent dataframe, sales dataframe
    OUTPUT: One bedroom rent dataframe with all zip codes of interest
    '''

    one_bed_added_zips = fill_missing_zips(one_bed_rent_df, sale_df, one_surrounding)
    return one_bed_added_zips


def apply_to_two_bed(two_bed_rent_df, sale_df):

    '''
    Fills in missing two bedroom zipcodes

    INPUT: Two bedroom rent dataframe, sales dataframe
    OUTPUT: Two bedroom rent dataframe with all zip codes of interest
    '''

    two_bed_added_zips = fill_missing_zips(two_bed_rent_df, sale_df, two_surrounding)
    return two_bed_added_zips

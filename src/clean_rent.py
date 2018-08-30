import pandas as pd
import numpy as np

seattle_zipcodes =  [98101, 98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109, 98112, 98115, 98116, 98117, 98118, 98119, 98121, 98122, 98125, 98126, 98133, 98136, 98144, 98177, 98199]

neighborhoods = {98101: 'Downtown', 98102: 'Captiol Hill', 98103: 'Wallingford', 98104: 'Pioneer Square', 98105: 'University District', 98106: 'Highland Park', 98107: 'Ballard', 98108: 'Georgetown/Beacon Hill', 98109: 'Westlake', 98112: 'Montlake', 98115 : 'Wedgewood', 98116: 'West Seattle/Alki', 98117: 'Crown Hill', 98118: 'Rainier Valley', 98119: 'Queen Anne', 98121: 'BellTown', 98122: 'Capitol Hill/Madrona', 98125: 'Lake City', 98126: 'West Seattle', 98133: 'North Park', 98136: 'Fauntleroy', 98144: 'Mt. Baker', 98177: 'Richmond Beach', 98199: 'Magnolia'}

def create_rent_df(rent_filepath):
    return pd.read_csv(rent_filepath)

def clean_rental_data(rent_filepath):
    rent_data = create_rent_df(rent_filepath)
    reduced_rent = rent_data[rent_data['RegionName'].isin(seattle_zipcodes)].copy()
    pruned_rent = reduced_rent.dropna(axis=1, how='all').copy()
    years=[]
    for num in range(2011,2018):
        years.append(str(num))
    for year in years:
        pruned_rent[year] = pruned_rent.loc[:, pruned_rent.columns.str.startswith(year)].median(axis=1)
    pruned_rent['neighborhood']= pruned_rent['RegionName'].map(neighborhoods)
    pruned_rent = pruned_rent.rename(columns={'RegionName':'zipcode'})
    clean_rent = pruned_rent.filter(items=['zipcode', 'neighborhood', *years]).reset_index(drop=True).copy()
    return clean_rent

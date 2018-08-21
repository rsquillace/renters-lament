import pandas as pd
import numpy as np

seattle_zipcodes = [98103, 98115, 98133, 98122, 98125, 98109, 98105, 98118, 98102, 98107, 98117, 98121, 98116, 98112, 98101, 98126, 98104]

neigborhoods = {98103: 'Wallingford', 98115 : 'Wedgewood',
                98133: 'North Park', 98122: 'Capitol Hill/Madrona',
                98125: 'Lake City', 98109: 'Westlake', 98105: 'University District',
                98118: 'Rainier Valley', 98102: 'Captiol Hill',
       98107: 'Ballard', 98117: 'Ballard', 98121: 'BellTown',
                98116: 'West Seattle/Alki', 98112: 'Montlake', 98101: 'Downtown',
                98126: 'West Seattle', 98104: 'Pioneer Square'}

def clean_rental_data(rent_filepath):
    rent_data = pd.read_csv(rent_filepath)
    reduced_rent = rent_data[rent_data['RegionName'].isin(seattle_zipcodes)].copy()
    pruned_rent = reduced_rent.dropna(axis=1, how='all').reset_index(drop=True).copy()
    years=[]
    for num in range(2011,2018):
        years.append(str(num))
    for year in years:
        pruned_rent[year] = pruned_rent.loc[:, pruned_rent.columns.str.startswith(year)].median(axis=1)
    pruned_rent['neighborhood']= pruned_rent['RegionName'].map(neigborhoods)
    clean_rent = pruned_rent.filter(items=['RegionName', 'neighborhood', *years])
    return clean_rent

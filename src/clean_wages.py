import pandas as pd
import numpy as np

def clean_wage(data_file_path,data_year):
    wages = pd.read_excel(data_file_path)
    clean_wages = wages.loc[:, list(wages.iloc[:,0:3])]
    clean_wages['avg_wage'] =  wages.iloc[:,18]
    clean_wages = clean_wages.rename(columns={clean_wages.columns[0]:'2_digit_naics', clean_wages.columns[1]:'3_digit_naics', clean_wages.columns[2]:'industry', clean_wages.columns[3]:'avg_wage'})
    clean_wages['3_digit_naics'] = clean_wages['3_digit_naics'].astype(str)
    clean_wages['2_digit_naics'] = clean_wages['2_digit_naics'].fillna(clean_wages['3_digit_naics'].str[:2])
    clean_wages['2_digit_naics'] = clean_wages[['2_digit_naics']].astype(str)
    clean_wages = clean_wages[clean_wages['2_digit_naics'] != 'na']
    clean_wages = clean_wages[clean_wages['avg_wage'] != '*'].reset_index(drop=True)
    clean_wages[['avg_wage']] = clean_wages[['avg_wage']].astype(int)
    clean_wages['monthly_rent_allowance'] = (clean_wages['avg_wage'] / 12)/3
    clean_wages['year'] = data_year
    return clean_wages

def make_min_wage_df(wage15,wage16,wage17, abbrev, desc):
    years = [2011,2012,2013,2014,2015,2016,2017]
    hourly_wage = np.array([8.76,9.04,9.19,9.32,wage15,wage16,wage17])
    avg_wage = (hourly_wage * 40) * 50
    min_wage_df = pd.DataFrame({'2_digit_naics': abbrev,
                                  '3_digit_naics': '',
                                  'industry': desc,
                                  'avg_wage': avg_wage,
                                  'monthly_rent_allowance': (avg_wage/12)/3,
                                  'year': years})
    return min_wage_df

def make_agg_wage_dataframe():
    dataframes = []
    for year in range(2011,2018):
        dataframes.append(clean_wage(f'data/king_county_wages_{year}.xls', year))
    dataframes.extend((make_min_wage_df(10, 10.5, 11, 'msb', 'Min Wage for Small Business w/ Bene or Tips'),
                      make_min_wage_df(11, 12, 13, 'ms', 'Min Wage for Small Business'),
                      make_min_wage_df(11, 12.5, 13.5, 'mlb', 'Min Wage for Lage Business w/ Bene'),
                      make_min_wage_df(11, 13, 15, 'ml', 'Min Wage for Large Business'))
                     )
    aggregated_wages = pd.concat(dataframes).reset_index(drop=True)
    return aggregated_wages

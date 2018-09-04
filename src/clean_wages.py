import pandas as pd
import numpy as np

def clean_wage(data_file_path,data_year):
    wages = pd.read_excel(data_file_path)
    wages = wages.dropna(subset=[wages.columns[1]])
    clean_wages = wages[wages.columns[[2, 18]]].copy()
    clean_wages = clean_wages.rename(columns={clean_wages.columns[0]:'industry', clean_wages.columns[1]:'avg_wage'})
    clean_wages = clean_wages[(clean_wages['avg_wage'] != '*')&(clean_wages['avg_wage'] != 0)].reset_index(drop=True)
    clean_wages['avg_wage'] = clean_wages['avg_wage'].astype(int)
    clean_wages['monthly_rent_allowance'] = (clean_wages['avg_wage'] / 12)/3
    clean_wages['year'] = data_year
    return clean_wages

def make_min_wage_df(wage15,wage16,wage17, desc):
    years = [2011,2012,2013,2014,2015,2016,2017]
    hourly_wage = np.array([8.76,9.04,9.19,9.32,wage15,wage16,wage17])
    avg_wage = (hourly_wage * 40) * 50
    min_wage_df = pd.DataFrame({'industry': desc,
                                  'avg_wage': avg_wage,
                                  'monthly_rent_allowance': (avg_wage/12)/3,
                                  'year': years})
    return min_wage_df

def make_agg_wage_dataframe():
    dataframes = []
    for year in range(2011,2018):
        dataframes.append(clean_wage(f'data/king_county_wages_{year}.xls', year))
    dataframes.extend((make_min_wage_df(10, 10.5, 11, 'Min Wage for Small Business w/ Bene or Tips'),
                      make_min_wage_df(11, 12, 13, 'Min Wage for Small Business'),
                      make_min_wage_df(11, 12.5, 13.5, 'Min Wage for Large Business w/ Bene'),
                      make_min_wage_df(11, 13, 15, 'Min Wage for Large Business'))
                     )
    aggregated_wages = pd.concat(dataframes, sort=False).reset_index(drop=True)
    v = aggregated_wages[['industry']]
    aggregated_wages = aggregated_wages[v.replace(v.apply(pd.Series.value_counts)).gt(5).all(1)]
    return aggregated_wages

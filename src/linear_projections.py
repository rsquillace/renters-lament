import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

def project_rent(filled_rent_df):
    filled_rent_df[['2018','2019','2020']] = pd.DataFrame(np.zeros([17,3]))
    year_columns = []
    for year in range(2011,2018):
        year_columns.append(str(year))
    years = np.array(range(2011,2018))
    pred_years = np.array([2018, 2019, 2020])
    train_x = years
    pred_dfs = []
    for zc in filled_rent_df['zipcode'].unique():
        y = filled_rent_df[filled_rent_df['zipcode'] == zc][[*year_columns]].values.T
        lr = LinearRegression()
        lr.fit(train_x.reshape(-1,1),y)
        pred_dic = {}
        for year in pred_years:
            test_pred = year
            pred_dic[str(year)] = [float(lr.predict(test_pred))]
        for year in pred_years:
            filled_rent_df.at[filled_rent_df['zipcode'] == zc, str(year)] = pred_dic[str(year)]
    return filled_rent_df

def project_wages(wage_df):
    ind_projection_dfs = []
    for ind in wage_df['industry'].unique():
        ind_wages = wage_df[wage_df['industry'] == ind].copy()
        years_of_interest = np.array(range(2011,2021))
        years_to_make = np.setdiff1d(years_of_interest, ind_wages['year'].values)
        x = np.transpose((ind_wages['year'].values, ind_wages['year'].values**2))
        y = ind_wages['avg_wage'].values
        lr = LinearRegression()
        lr.fit(x,y)
        pred_dic = {}
        for year in years_to_make:
            test_pred = np.array([[year, year**2]])
            pred_dic[year] = float(lr.predict(test_pred))
        new_rows = []
        for k,v in pred_dic.items():
            row = [ind, v, (v/12)/3 , k]
            new_rows.append(row)
        new_ind_df = pd.DataFrame(new_rows, columns = ind_wages.columns)
        ind_projection_dfs.append(pd.concat((ind_wages, new_ind_df)))
    return pd.concat(ind_projection_dfs).reset_index(drop=True)

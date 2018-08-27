import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

def predict_rent(filled_rent_df):
    filled_rent_df[['2018','2019','2020']] = pd.DataFrame(np.zeros([17,3]))
    year_columns = []
    for year in range(2011,2018):
        year_columns.append(str(year))
    years = np.array(range(2011,2018))
    pred_years = np.array([2018, 2019, 2020])
    train_x = np.transpose(np.stack((years, years**2)))
    pred_dfs = []
    for zc in filled_rent_df['zipcode'].unique():
        y = filled_rent_df[filled_rent_df['zipcode'] == zc][[*year_columns]].values.T
        lr = LinearRegression()
        lr.fit(train_x,y)
        pred_dic = {}
        for year in pred_years:
            test_pred = np.array([[year, year**2]])
            pred_dic[str(year)] = [float(lr.predict(test_pred))]
        for year in pred_years:
            filled_rent_df.at[filled_rent_df['zipcode'] == zc, str(year)] = pred_dic[str(year)]
    return filled_rent_df

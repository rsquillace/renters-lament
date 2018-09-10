import pandas as pd
import numpy as np
from pyramid.arima import auto_arima


def transform_df(rent_df, zipcode, start_year,end_year):

    '''
    Reformats rent dataframe so ARIMA models can be applied

    INPUT: Rent dataframe, zip code of interest, earliest known year of rent, latest known year of rent
    OUTPUT: Reformatted rent dataframe for zip code of interest
    '''

    years = []
    for year in range(start_year,end_year+1):
        years.append(str(year))
    zip_df = rent_df[rent_df['zipcode'] == zipcode].loc[:, str(start_year):str(end_year)].T.copy()
    return zip_df


def make_rent_arima_predictions(rent_df, start_year, end_year, year_to_predict_to):

    '''
    Fits ARIMA model and makes projections for rent, adds projections to rent dataframe

    INPUT: Rent dataframe, earliest known year of rent, latest known year of rent, year to predict through
    OUTPUT: Rent dataframe with added projections
    '''

    pred_rent = rent_df.copy()
    pred_years = []
    for year in range(end_year+1, year_to_predict_to+1):
        pred_years.append(str(year))
    num_pred_years = year_to_predict_to - end_year
    pred_rent[pred_years] = pd.DataFrame(np.zeros([len(pred_rent),num_pred_years]))
    for zc in pred_rent['zipcode'].unique():
        df = transform_df(pred_rent, zc, start_year,end_year)
        model = auto_arima(df, start_p=1, start_q=1, start_P=1, start_Q=1,
                      max_p=5, max_q=5, max_P=5, max_Q=5, seasonal=False,
                      stepwise=True, suppress_warnings=True,
                      error_action='ignore')
        predictions, confidence_interval = model.predict(n_periods=num_pred_years,return_conf_int=True)
        pred_dic = {}
        for i in range(num_pred_years):
            pred_dic[pred_years[i]] = predictions[i]
        for year in pred_years:
            pred_rent.at[pred_rent['zipcode'] == zc, str(year)] = pred_dic[str(year)]
    return pred_rent


def make_wage_arima_predictions(wage_df, start_year, year_to_predict_to):

    '''
    Fits ARIMA model and make projections for wages, adds projections to wage dataframe

    INPUT: Wage dataframe, earliest considered wage year, year to predict through
    OUTPUT: Wage dataframe with added projections
    '''

    ind_projection_dfs = []
    l = []
    for ind in wage_df['industry'].unique():
        ind_wages = wage_df[wage_df['industry'] == ind].copy()
        years_of_interest = np.array(range(start_year,year_to_predict_to+1))
        years_to_make = np.setdiff1d(years_of_interest, ind_wages['year'].values)
        x = ind_wages['year'].values
        y = ind_wages['avg_wage'].values/100
        ind_df = pd.DataFrame(y.T, index = x)
        model = auto_arima(ind_df, start_p=1, start_q=1, start_P=1, start_Q=1,
                      max_p=5, max_q=5,max_P=5, max_Q=5, seasonal=False,
                      stepwise=True, suppress_warnings=True,
                      error_action='ignore')
        predictions, confidence_interval = model.predict(n_periods=len(years_to_make),return_conf_int=True)
        pred_dic = {}
        for i in range(len(years_to_make)):
            pred_dic[years_to_make[i]] = predictions[i]*100
        new_rows = []
        for k,v in pred_dic.items():
            row = [ind, v, (v/12)/3 , k]
            new_rows.append(row)
        new_ind_df = pd.DataFrame(new_rows, columns = ind_wages.columns)
        ind_projection_dfs.append(pd.concat((ind_wages, new_ind_df)))
    return pd.concat(ind_projection_dfs).reset_index(drop=True)

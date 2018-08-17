import pandas as pd

def wage_data_cleaner(data_file_path,data_year):
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

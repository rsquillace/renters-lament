import pandas as pd

def wage_data_cleaner(data_file_path,data_year):
    wages = pd.read_excel(data_file_path)
    clean_wages = wages.loc[:, list(wages.iloc[:,0:3]) + list(wages.iloc[:,16:19])]
    clean_wages = clean_wages.rename(columns={clean_wages.columns[0]:'2_digit_naics', clean_wages.columns[1]:'3_digit_naics', clean_wages.columns[2]:'industry', clean_wages.columns[3]:'total_wages', clean_wages.columns[4]:'avg_employment',clean_wages.columns[5]:'avg_wage'})
    clean_wages['3_digit_naics'] = clean_wages['3_digit_naics'].astype(str)
    clean_wages['2_digit_naics'] = clean_wages['2_digit_naics'].fillna(clean_wages['3_digit_naics'].str[:2])
    clean_wages['2_digit_naics'] = clean_wages[['2_digit_naics']].astype(str)
    clean_wages = clean_wages[clean_wages['2_digit_naics'] != 'na']
    clean_wages = clean_wages[clean_wages['avg_wage'] != '*'].reset_index(drop=True)
    clean_wages['year'] = data_year
    clean_wages[['total_wages','avg_employment','avg_wage','year']] = clean_wages[['total_wages','avg_employment','avg_wage','year']].astype(int)
    return clean_wages

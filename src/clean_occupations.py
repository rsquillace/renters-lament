import pandas as pd
import numpy as np

def clean_year_df(occupation_year_filepath, year):
    occ_df = pd.read_csv(occupation_year_filepath)
    start_row = occ_df.loc[occ_df.iloc[:, 1] == 'Accountants & Auditors'].index.values[0]
    pruned_occ = occ_df.drop(occ_df.index[range(0,start_row)])[occ_df.columns[[1,2,7]]].copy()
    pruned_occ = pruned_occ.rename(columns = {pruned_occ.columns[0]: 'title', pruned_occ.columns[1]: 'est_emp', pruned_occ.columns[2]:'ann_wage'})
    clean_occ = pruned_occ.dropna(subset=['est_emp','ann_wage']).copy()
    clean_occ[['ann_wage', 'est_emp']] = clean_occ[['ann_wage', 'est_emp']].astype(str)
    for char in ['$', ',']:
        clean_occ['ann_wage'] = clean_occ['ann_wage'].str.replace(char, '')
        clean_occ['est_emp'] = clean_occ['est_emp'].str.replace(char, '')
    clean_occ[['ann_wage', 'est_emp']] = clean_occ[['ann_wage', 'est_emp']].astype(int)
    final_occ = clean_occ.nlargest(300, 'est_emp').copy().reset_index(drop=True)
    final_occ['year'] = year
    return final_occ

def aggregate_occupations(start_year, end_year, num_years):
    occ_dfs = []
    for year in range(start_year, end_year+1):
        occ_dfs.append(clean_year_df(f'data/occupations{year}.csv', year))
    aggregated_occs = pd.concat(occ_dfs, sort=False).reset_index(drop=True)
    occupations = aggregated_occs[['title']]
    aggregated_occs = aggregated_occs[occupations.replace(occupations.apply(pd.Series.value_counts)).gt(num_years-1).all(1)].reset_index(drop=True)
    return aggregated_occs

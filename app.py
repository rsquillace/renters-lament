from flask import Flask, render_template, jsonify
from random import random
import pandas as pd
import numpy as np

merged = pd.read_csv('data/aggregated_affordability/affordability_data_with_projections.csv')
merged['zipcode'] = merged['zipcode'].astype(str)
app = Flask(__name__)

@app.route('/')
def index():
    industry_names = merged['industry'].unique()
    years = merged['year'].unique()
    bedrooms = merged['bedrooms'].unique()
    return render_template('index.html', years=years, industry_names=industry_names, bedrooms=bedrooms)

@app.route('/table/<industry_name>/<year>/<bedroom>')
def table(industry_name, year, bedroom):
    zips = retrieve_affordable_zips(industry_name, int(year), int(bedroom))
    #n = len(zips)
    x = zips
    #y = zips
    return render_template('table.html', data=x)

@app.route('/map_data/<industry_name>/<year>/<bedroom>')
def aff_map(industry_name, year, bedroom):
    df = merged[merged['industry'] == industry_name]
    df = df[df['year'] == int(year)]
    df = df[df['bedrooms'] == int(bedroom)]
    zip_info = {}
    for zip in df['zipcode'].values:
        if df[df['zipcode'] == zip]['affordable'].item() == True:
            zip_info[zip] = '#58D68D'
        else:
            zip_info[zip] = '#FF5858'
    return jsonify(zip_info)


def retrieve_affordable_zips(industry_name, year, bedroom):
    df = merged[(merged['industry'] == industry_name)&(merged['year'] == year)&(merged['bedrooms'] == bedroom)].copy()
    affordable_zips = []
    for zip in df['zipcode'].values:
        if df[df['zipcode'] == zip]['affordable'].item() == True:
            affordable_zips.append(zip)
    return affordable_zips

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)

from flask import Flask, render_template, jsonify
from random import random
import pandas as pd
import numpy as np

merged = pd.read_csv('data/affordability_data.csv')
merged['zipcode'] = merged['zipcode'].astype(str)
app = Flask(__name__)

@app.route('/')
def index():
    industry_names = merged['industry'].unique()
    years = merged['year'].unique()
    return render_template('index.html', years=years, industry_names=industry_names)

@app.route('/table/<industry_name>/<year>')
def table(industry_name, year):
    zips = retrieve_affordable_zips(industry_name, int(year))
    #n = len(zips)
    x = zips
    #y = zips
    return render_template('table.html', data=x)

@app.route('/map_data/<industry_name>/<year>')
def aff_map(industry_name, year):
    df = merged[(merged['industry'] == industry_name)&(merged['year'] == year)].copy()
    zip_info = []
    for zip in df['zipcode'].values:
        zip_dic = {}
        zip_dic['zipcode'] = zip
        if df[df['zipcode'] == zip]['affordable'].item() == True:
            zip_dic['color'] = '#58D68D'
            zip_dic['label'] = 'affordable'
        else:
            zip_dic['color'] = '#D5D8DC'
            zip_dic['label'] = 'not affordable'
        zip_info.append(zip_dic)
    return render_template('map.html', jsonify(zip_info))


def retrieve_affordable_zips(industry_name, year):
    df = merged[(merged['industry'] == industry_name)&(merged['year'] == year)].copy()
    affordable_zips = []
    for zip in df['zipcode'].values:
        if df[df['zipcode'] == zip]['affordable'].item() == True:
            affordable_zips.append(zip)
    return affordable_zips

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

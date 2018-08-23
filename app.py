from flask import Flask, render_template
from random import random
import pandas as pd
import numpy as np

merged = pd.read_csv('data/affordability_data.csv')
app = Flask(__name__)


@app.route('/')
def index():
    n = 100
    x = range(n)
    y = [random() for i in x]
    return render_template('table.html', data=zip(x, y))

@app.route('/table/<industry_name>/<year>')
def table(industry_name, year):
    zips = retrieve_affordable_zips(merged, industry_name, int(year))
    n = len(zips)
    x = range(n)
    y = zips
    return render_template('table.html', data=zip(x, y))

def retrieve_affordable_zips(merged, industry_name, year):
    aff = merged.loc[:, merged.columns.str.startswith('98')].loc[(merged['industry'] == industry_name)&(merged['year'] == year)].values[0]
    zips = merged.loc[:, merged.columns.str.startswith('98')].columns
    return zips[aff]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

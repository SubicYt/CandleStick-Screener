
from flask import Flask, render_template, request
from patterns import patterns

import yfinance as yf
import os
import pandas as pd
import talib

app = Flask(__name__)

@app.route("/")
def index():
    pattern = request.args.get("pattern",None)
    if pattern:
        datafiles = os.listdir("datasets/daily")
        for dataset in datafiles:
            df = pd.read_csv('datasets/daily/{}'.format(dataset))
            pattern_function = getattr(talib,pattern)
            try:
                result = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                print(result)
            except:
                pass
    return render_template('index.html', patterns = patterns)

@app.route("/snapshot")
def snapshot():
    with open('datasets/companies.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]
            df = yf.download(symbol, start='2024-01-01', end='2024-08-01')
            df.to_csv('datasets/daily/{}.csv'.format(symbol))

    return{
        'code':'success'
    }
if __name__ == ("__main__"):
    app.run(debug=True)
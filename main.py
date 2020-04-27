from __future__ import absolute_import
from flask import Flask, render_template, flash, request, jsonify
import json
import logging
import datetime
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()
import requests
import matplotlib.pyplot as plt
import lib.numpy
import pandas as pd

# [START create_app]
app = Flask(__name__, static_url_path='/static')
# [END create_app]

# [START form]
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
# [END form]


@app.route('/forecast', methods=['GET', 'POST'])
def morning():
    url="https://forecaste.uc.r.appspot.com/update_open"
    with requests.request("GET",url,stream=True) as response:
        df = response.json()
        df1 = pd.read_json(df)
        fig,ax = plt.subplots(figsize=(15,10))
        plt.plot(df1['open'],c='b')
        plt.plot(df1['[pred_open]'],c='r')
        ax.legend(["Actual Open", "Predicted Open"])
        ax.set_ylabel("Actual vs. Predicted", fontsize=35)
        pred = df1.iloc[-1]['pred_open']
        plt.savefig('static/images/graph.png')

        if pred > df1.iloc[-2]['open']:
            signal = "BUY"
        elif pred <= df1.iloc[-2]['open']:
            signal = "HOLD"

        return render_template('forecast.html',pred=pred,signal=signal)

# [START form]
@app.route('/poster')
def evening():
    return render_template('poster.html')
# [END form]



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]

def get_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

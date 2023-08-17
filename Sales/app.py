import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset
import matplotlib.pyplot as plt
# %matplotlib inline
from io import BytesIO
import base64
import seaborn as sns
from seaborn.regression import statsmodels
from statsmodels.tsa.stattools import adfuller
from pandas.plotting import autocorrelation_plot
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.arima_model import ARIMA

app = Flask(__name__)

def generate_plot(df, column_name):
    plt.figure(figsize=(12, 8))
    plt.plot(df[column_name], label=column_name)
    plt.legend()
    plt.title(column_name)
    plt.xlabel('Date')
    plt.ylabel('Value')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return graph_url


@app.route('/', methods=['GET', 'POST'])
def index():
    plot_urls = []

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            df['Month'] = pd.to_datetime(df['Month'])
            df.set_index('Month', inplace=True)

            # Plot 1
            plot_urls.append(generate_plot(df, 'Sales'))

            # Plot 2
            df['Seasonal First Difference'] = df['Sales'] - df['Sales'].shift(12)
            plt.figure()
            autocorrelation_plot(df['Sales'])
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_urls.append(base64.b64encode(img.getvalue()).decode())

            # Plot 3
            fig = plt.figure()
            ax1 = fig.add_subplot(211)
            fig = sm.graphics.tsa.plot_acf(df['Seasonal First Difference'].iloc[13:], lags=40, ax=ax1)
            ax2 = fig.add_subplot(212)
            fig = sm.graphics.tsa.plot_pacf(df['Seasonal First Difference'].iloc[13:], lags=40, ax=ax2)
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_urls.append(base64.b64encode(img.getvalue()).decode())

            # Plot 4
            model = sm.tsa.arima.ARIMA(df['Sales'], order=(0, 0, 1))
            model_fit = model.fit()
            df['forecast_arima'] = model_fit.predict(start=90, end=103, dynamic=True)
            
            model = sm.tsa.statespace.SARIMAX(df['Sales'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
            results = model.fit()
            df['forecast_sarimax'] = results.predict(start=90, end=103, dynamic=True)
            
            future_dates = [df.index[-1] + DateOffset(months=x) for x in range(0, 24)]
            future_df = pd.DataFrame(index=future_dates[1:], columns=df.columns)
            future_df = pd.concat([df, future_df])
            future_df['forecast_sarimax'] = results.predict(start=104, end=120, dynamic=True)
            
            plot_urls.append(generate_plot(future_df, 'forecast_sarimax'))
            
    return render_template('index.html', plot_urls=plot_urls)

if __name__ == '__main__':
    app.run(debug=True)
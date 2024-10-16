import datetime
import sys
from time import sleep

import pandas as pd
from datetime import date
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as graf

def load_free_data(ticker, start='2024-10-01', end='2024-10-11»', interval = '1h'):
    end = date.today()
    stock = yf.Ticker(ticker)
    data = stock.history(start="2024-10-10", end="2024-10-11", interval="1m")
    return data

def create_and_save_plot_fr(data, ticker, period, filename=None):

    plt.clf()
    #fg=plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')

            #plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])

        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
    current_time = datetime.datetime.now().time()
    plt.title(f" {ticker} Цена акций с течением времени\n, (Текущее время) {current_time}")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()
    ff = graf.Figure()

    plt.grid(True)
    #plt.annotate('Пример текста', xy=(dates[2], data['Close'][2]), arrowprops=dict(facecolor='red', shrink=0.006),
    #             xytext=(dates[1], data['Close'][9]))


    plt.draw()
    plt.gcf().canvas.flush_events()
    sleep(5)
    plt.close("all")
    #plt.show()

    return



    #if filename is None:
    #    filename = f"{ticker}_{period}_stock_price_chart.png"

    #plt.savefig(filename)
    #print(f"График сохранен как {filename}")


import datetime
import os
from pathlib import Path

import pandas as pd
from datetime import date
import yfinance as yf
import matplotlib.pyplot as plt
import log_conf
import main


def calculate_and_display_average_price(data):
    '''Функция выводит среднюю цену закрытия акций за заданный период'''
    middle = data['Close'].mean()
    mess = f'Средняя цена = {middle}'
    log_conf.logging.info(mess)
    return middle


def notify_if_strong_fluctuations(data, threshold):
    '''Функция анализирует данные и уведомляет пользователя,
    если цена акций изменялась более чем на заданный процент за период'''

    percent = (data['Close'].max() - data['Close'].min()) / data['Close'].mean() * 100
    if percent >= threshold:
        # print(f'цена акций колебалась на {percent}%')
        mess = f'Изменение цены больше нормы: {percent:.2f}'
        log_conf.logging.info(mess)
        return percent
    return None


def export_data_to_csv(data, filename=None):
    ''' функция export_data_to_csv(data, filename),
     которая позволяет сохранять загруженные данные об акциях в CSV файл
     '''
    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d время %H-%M-%S')
    if filename is None:
        filename = f"OUT\{formatted_date} data.csv"
    else:
        filename = f"OUT\{filename} data.csv"
    try:
        data.to_csv(filename, sep=',', index=True, encoding='windows-1251')
        message = f"Данные выгружены в {filename}"
        log_conf.logging.info(message)
    except Exception as error_pd:
        message = f'Ошибка {error_pd}'
        print(f'Ошибка {message}')
        log_conf.logging.info(message)


def add_technical_indicators(data):
    '''Функция добавляет дополнительный технический индикатор RSI'''

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data


def create_and_save_plot_with_indicators(data, ticker, period, filename=None):
    ''' Функция выводит график цен в одном  и во втором технический индикатор привязанный
    к шкале времени'''
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 6))
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            # график цен
            axs[0].plot(dates, data['Close'].values, label='Prices')
            axs[0].plot(dates, data['Moving_Average'], label='Moving Average')
            # график RSI
            axs[1].plot(dates, data['RSI'], label='RSI')
            axs[1].axhline(y=70, color='r', linestyle='--')
            axs[1].axhline(y=30, color='g', linestyle='--')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
            # график цен
            axs[0].plot(data['Date'], data['Close'].values, label='Prices')
            axs[0].plot(data['Date'], data['Moving_Average'], label='Moving Average')

            # график RSI
            axs[1].plot(data['Date'], data['RSI'], label='RSI')
            axs[1].axhline(y=70, color='r', linestyle='-')
            axs[1].axhline(y=30, color='g', linestyle='-')

    axs[0].set_title(f"{ticker} Цена акций с течением времени", fontsize=10)
    axs[0].set_xlabel('Дата')
    axs[0].set_ylabel('Цена')
    axs[0].grid(True)

    axs[1].set_title("Индикатор RSI", fontsize=10)
    axs[1].grid(True)

    plt.show()
    pass

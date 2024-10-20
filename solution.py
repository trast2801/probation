import datetime

import pandas as pd
from datetime import date
import yfinance as yf
import log_conf
import main


def calculate_and_display_average_price(data):
    '''Функция выводит среднюю цену закрытия акций за заданный период'''
    return data['Close'].mean()


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

    if filename is None:
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d время %H-%M-%S')
        filename = f"{formatted_date} data.csv"

    try:
        data.to_csv(filename, sep=',', index=False, encoding='utf-8')
        message = f"Данные выгружены в {filename}"
        log_conf.logging.info(message)
    except Exception as error_pd:
        message = f'Ошибка {error_pd}'
        log_conf.logging.info(message)


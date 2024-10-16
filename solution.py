import pandas as pd
from datetime import date
import yfinance as yf

def calculate_and_display_average_price(data):
    '''Функция выводит среднюю цену закрытия акций за заданный период'''
    return data['Close'].mean()


def notify_if_strong_fluctuations(data, threshold):
    '''Функция анализирует данные и уведомляет пользователя,
    если цена акций изменялась более чем на заданный процент за период'''

    percent = (data['Close'].max() - data['Close'].min()) / data['Close'].mean() * 100
    if percent >= threshold:
        #print(f'цена акций колебалась на {percent}%')
        return percent
    return None
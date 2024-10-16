import sys
from time import sleep

import data_download as dd
import data_plotting as dplt
import solution as sl
import freestyle as fr
import matplotlib.pyplot as plt
import signal

def handler(signum, frame):
    print("Вы нажали CTRL+C")
    sys.exit(1)


def first():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    middle = sl.calculate_and_display_average_price(stock_data)
    otklonenie = sl.notify_if_strong_fluctuations(stock_data, 5)
    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)



    print(f'Среднее за период: {middle:.2f}\n'
          f'Отклонение выше норматива: {otklonenie:.2f}')

def second():
    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    ticker="AAPL"
    print("Переходим в режим ежеминутной прорисовки графика, для выхода закроте окно")
    plt.ion()

    while True:
        signal.signal(signal.SIGINT, handler)
        stock_data = fr.load_free_data(ticker)
        stock_data = dd.add_moving_average(stock_data)
        fr.create_and_save_plot_fr(stock_data, ticker, period='1mo')
    plt.ioff()

def main():
    while True:
        key = input("Выберите режим:\n 1 - по ТЗ\n 2 - Вольное творчество(идея интерактива, не статичные графики) \n 3 - выход : ")
        #key="2"
        if key == "1":
            first()
        if key == "2":
            second()
        if key == "3":
            break


if __name__ == "__main__":
    main()

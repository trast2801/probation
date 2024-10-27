from datetime import datetime, timedelta, date
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import log_conf



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
    now = datetime.now()
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


def create_and_save_plot_with_indicators(data, ticker, period, style, filename=None):
    ''' Функция выводит график цен в одном  и во втором технический индикатор привязанный
    к шкале времени'''
    plt.style.use(style)
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

    if filename is None:
        filename = f"OUT\{ticker}_New_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")
    plt.show()
    plt.close()
    pass

def entering_an_arbitrary_period():
    ''' ввод проивольного периода для загрузки дат '''
    period = {
        'start_date' : None,
        'end_date' : None
    }
    period_input = input(
        "Введите период для данных (например, '2024-01-01 2024-12-31' для данных за 2024 год, или '1mo' для одного "
        "месяца) \n"
        "(Ещё варианты: 1d, 5d, 1mo, 3moс, 6mo, 1y, 2y, 5y, 10y, с начала года, max: ")

    '''Обработка ввода пользователя'''
    if '-' in period_input:
        start_date, end_date = period_input.split()
        period['start_date'] = datetime.strptime(start_date, "%Y-%m-%d")
        period['end_date'] = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        period_map = {
            '1d': pd.Timedelta(days=1),
            '5d': pd.Timedelta(days=5),
            '1mo': pd.Timedelta(weeks=4),
            '3mo': pd.Timedelta(weeks=12),
            '6mo': pd.Timedelta(weeks=24),
            '1y': pd.Timedelta(weeks=52),
            '2y': pd.Timedelta(weeks=104),
            '5y': pd.Timedelta(weeks=260),
            '10y': pd.Timedelta(weeks=520),
            'max': None
        }

        if period_input == 'max':
            period['start_date'] = datetime.strptime('1970/01/01', '%Y/%m/%d')
            period['end_date'] = datetime.now()
        elif period_input == '1d':
            period = None
        elif period_input in period_map:
            period['start_date'] = datetime.now() - period_map[period_input]
            period['end_date'] = datetime.now()
        elif period_input == 'с начала года':
            period['start_date'] = datetime.now().replace(month=1, day=1)
            period['end_date'] = datetime.now()
        else:

            period = None


    return period

def fetch_stock_data_new(ticker, start_date, end_date):
    '''Функция получает исторические данные об акциях для указанного тикера и временного периода. Возвращает DataFrame
     с данными.'''
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data

def choise_style():
    '''Функция проверяет выбранный стиль и возвращет значение или стиль по умолчанию'''
    spisok = ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh',
     'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot',
     'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind',
     'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep',
     'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel',
     'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid',
     'tableau-colorblind10']
    style = input ('Введите название стиля, например (classic, dark_background, fast), по умолчанию classic:')
    if style in spisok:
        return style
    else:
        style = 'classic'
        return style
    pass
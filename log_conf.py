import logging

# формат вывода лога

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s', encoding='WINDOWS-1251',
                    datefmt='%Y-%m-%d %H:%M:%S')



import logging
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)


class Logger:
    LEVEL_COLORS = {
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'DBG': Fore.CYAN,
        'INPUT': Fore.MAGENTA
    }

    def __init__(self, name='ColoredLogger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log(self, level, message):
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        color = self.LEVEL_COLORS.get(level, Fore.WHITE)
        log_message = f"{color}[{now.split()[1]}] [{level}]{Style.RESET_ALL} {message}"
        colored_message = f"{log_message}"
        self.logger.debug(colored_message)

    def info(self, message):
        self.log('INFO', message)

    def warning(self, message):
        self.log('WARN', message)

    def error(self, message):
        self.log('ERR', message)

    def debug(self, message):
        self.log('DBG', message)

    def input(self, prompt):
        time.sleep(0.2)
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        color = self.LEVEL_COLORS.get('INPUT', Fore.WHITE)
        log_message = f"{color}[{now.split()[1]}] [INPT]{Style.RESET_ALL} {prompt}"
        print(log_message, end='')
        return input('')


log = Logger()


import logging
import sys


class Logger:
    def __new__(cls):
        _logger = logging.getLogger('internal')
        ch = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        _logger.addHandler(ch)
        return _logger


logger = Logger()


class Console:
    def print(self, text, *, sep=' ', end='\n'):
        print(text, sep=sep, end=end)

    def error(self, text, *, sep=' ', end='\n'):
        print(text, file=sys.stderr, sep=sep, end=end)


console = Console()

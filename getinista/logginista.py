import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    base_format = u'[%(asctime)s] [%(levelname)-8s] %(message)s [%(filename)s:%(lineno)d]'

    FORMATS = {
        logging.DEBUG: grey + base_format + reset,
        logging.INFO: grey + base_format + reset,
        logging.WARNING: yellow + base_format + reset,
        logging.ERROR: red + base_format + reset,
        logging.CRITICAL: bold_red + base_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger("sessionista")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

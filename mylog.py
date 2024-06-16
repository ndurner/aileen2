import logging.config

def setup_logging():
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

def getLogger(name: str) -> logging.Logger:
    return logging.getLogger("app." + name)
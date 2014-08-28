import logging
import logging.config
import os

path = os.getcwd()
logging.config.fileConfig('logger.cfg')

# create logger
root_logger = logging.getLogger()


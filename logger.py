from aiohttp import log
import logging
import sys

access_logger = log.access_logger
access_logger.setLevel(logging.INFO)
# formatter = logging.Formatter(fmt='%a %l %u %t "%r" Data:"%O" %s %b "%{Referrer}i" "%{User-Agent}i"')
stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler.setFormatter(fmt='%a %l %u %t "%r" Data:"%O" %s %b "%{Referrer}i" "%{User-Agent}i"')
file_handler = logging.FileHandler('access_logs')
access_logger.addHandler(stream_handler)
access_logger.addHandler(file_handler)

server_logger = log.server_logger
server_logger.setLevel(logging.INFO)
server_stream_handler = logging.StreamHandler(sys.stdout)
server_file_handler = logging.FileHandler('server_logs')
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] in %(pathname)s --> %(funcName)s --> %(message)s')
server_file_handler.setFormatter(formatter)
server_stream_handler.setFormatter(formatter)
server_logger.addHandler(server_stream_handler)
server_logger.addHandler(server_file_handler)



class DbHandler(logging.Handler):
    def __init__(self, db, *args, **kwargs):
        super(DbHandler, self).__init__(*args, **kwargs)
        self.db = db

    def emit(self, record):
        pass
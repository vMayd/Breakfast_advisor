import asyncio

import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aioredis import create_pool
from settings import COOKIE_AGE, COOKIE_AUTH_NAME

from logger import access_logger, server_logger
from db_auth import DBAuthorizationPolicy
from routes import *
from motor import motor_asyncio

loop = asyncio.get_event_loop()
redis_pool = loop.run_until_complete(create_pool(('localhost', 6379)))
client = motor_asyncio.AsyncIOMotorClient('localhost', 27017)

# Initiate main application
app = web.Application(loop=loop, logger=server_logger)
setup_routes(app, 'main')
setup_static(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'))

# Initiate sub-applications
admin = web.Application(loop=loop, logger=server_logger)
setup_routes(admin, 'admin')
aiohttp_jinja2.setup(admin, loader=jinja2.FileSystemLoader('templates/'))
setup_session(admin, RedisStorage(redis_pool, max_age=COOKIE_AGE, cookie_name=COOKIE_AUTH_NAME))
setup_security(admin, SessionIdentityPolicy(), DBAuthorizationPolicy())

app.add_subapp('/admin/', admin)

api = web.Application(loop=loop, logger=server_logger)
setup_routes(api, 'api')
app.add_subapp('/api/', api)

# Session and security
setup_session(app, RedisStorage(redis_pool, max_age=COOKIE_AGE, cookie_name=COOKIE_AUTH_NAME))
setup_security(app, SessionIdentityPolicy(), DBAuthorizationPolicy())

# Run server
web.run_app(app=app, host=settings.HOST, port=settings.PORT, access_log=access_logger,
            access_log_format='%a %l %u %t "%r" %s %b "%{Referrer}i" "%{User-Agent}i"')

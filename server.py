import asyncio
import aiohttp_jinja2
import aiohttp
import jinja2
from aiohttp import web
from routes import *

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
setup_routes(app)
setup_static(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'))
web.run_app(app=app, host='localhost', port=8080)

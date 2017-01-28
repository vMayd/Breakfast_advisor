from aiohttp import web
from models.helper import get_items
from models.model import dishes
from validator import *


# logger = log.server_logger
# h
# logger.addHandler()

class Handler:
    def __init__(self):
        pass


    async def recipe(self, request):
        data = await request.json()
        name = request.match_info.route.name
        try:
            validate(name, data)
        except jsonschema.ValidationError as e:
            return web.HTTPBadRequest(reason='%s: %s' % ('Validation error', e.message))
        result = get_items(dishes, data)
        return web.json_response({'response': result})

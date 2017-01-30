from aiohttp import web
from aiohttp.web import View

from models.helper import get_items, cursor_to_list
from models.model import dishes
from validator import *

projection = {
    '_id': False,
    'ingredients_en': True,
    'name_en': True,
    'cooking_time': True,
    'image_url': True
}


class DishApi(View):
    async def post(self):
        return await self.recipe(self.request)

    async def recipe(self, request):
        data = await request.json()
        name = request.match_info.route.name
        try:
            validate(name, data)
        except jsonschema.ValidationError as e:
            return web.HTTPBadRequest(reason='%s: %s' % ('Validation error', e.message))
        result = get_items(dishes, data)
        return web.json_response({'response': result})


class Drinks(View):
    async def get(self):
        return await self.get_drinks(self.request)

    async def get_drinks(self, request):
        drinks = dishes.find(filter={'category': 'drink'}, projection=projection)
        return web.json_response(cursor_to_list(drinks))


class MainDish(View):
    async def get(self):
        return await self.get_main(self.request)

    async def get_main(self, request):
        main = dishes.find(filter={'category': 'main_dish'}, projection=projection)
        return web.json_response(cursor_to_list(main))


class FirstDish(View):
    async def get(self):
        return await self.get_first(self.request)

    async def get_first(self, request):
        first = dishes.find(filter={'category': 'second_1'}, projection=projection)
        return web.json_response(cursor_to_list(first))


class SecondDish(View):
    async def get(self):
        return await self.get_second(self.request)

    async def get_second(self, request):
        second = dishes.find(filter={'category': 'second_2'}, projection=projection)
        return web.json_response(cursor_to_list(second))

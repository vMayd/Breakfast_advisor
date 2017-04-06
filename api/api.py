from aiohttp import web
from aiohttp.web import View

from models.helper import parse_query_args
from models.model import Dish
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
        query = parse_query_args(data)
        cursor = Dish.collection.find(query, projection=projection)
        result_list = await cursor.to_list(length=1000)
        return web.json_response({'response': result_list})


class Drinks(View):
    async def get(self):
        return await self.get_drinks(self.request)

    async def get_drinks(self, request):
        cursor = Dish.collection.find({'category': 'drink'}, projection=projection)
        result_list = await cursor.to_list(length=1000)
        return web.json_response(result_list)


class MainDish(View):
    async def get(self):
        return await self.get_main(self.request)

    async def get_main(self, request):
        cursor = Dish.collection.find({'category': 'main_dish'}, projection=projection)
        result_list = await cursor.to_list(length=1000)
        return web.json_response(result_list)


class FirstDish(View):
    async def get(self):
        return await self.get_first(self.request)

    async def get_first(self, request):
        cursor = Dish.collection.find({'category': 'second_1'}, projection=projection)
        result_list = await cursor.to_list(length=1000)
        return web.json_response(result_list)


class SecondDish(View):
    async def get(self):
        return await self.get_second(self.request)

    async def get_second(self, request):
        cursor = Dish.collection.find({'category': 'second_2'}, projection=projection)
        result_list = await cursor.to_list(length=1000)
        return web.json_response(result_list)

import functools

import aiohttp_jinja2
import asyncio

from aiohttp import web
from aiohttp.web import View
from aiohttp_security import permits, forget
from pymongo.errors import InvalidOperation

from helper import save_image
from models.model import User, Dish
import settings


def require(permission):
    def wrapper(f):
        @asyncio.coroutine
        @functools.wraps(f)
        def wrapped(self, request):
            has_perm = yield from permits(request, permission)
            if not has_perm:
                response = web.HTTPFound('/login/')
                return response
            return (yield from f(self, request))
        return wrapped
    return wrapper


class Users(View):
    async def get(self):
        return await self.get_index(self.request)

    @require('admin')
    @aiohttp_jinja2.template('users.html')
    async def get_index(self, request):
        user_list = await User.find()
        return {'users': user_list}


class CreateItem(View):

    async def get(self):
        return await self.get_resp(self.request)

    async def post(self):
        return await self.post_resp(self.request)

    @require('admin')
    @aiohttp_jinja2.template('create_item.html')
    async def get_resp(self, request):
        choices = Dish.CATEGORIES
        return {'choices': choices}

    @require('admin')
    @aiohttp_jinja2.template('create_item.html')
    async def post_resp(self, request):
        data = await request.post()
        data_dict = self.post_data_to_dict(data)
        if data['image']:
            data_dict.pop('image')
            image = data['image']
            image_file = image.file
            filename = image.filename
            path = '%s/%s' % (settings.IMAGE_DIRECTORY.rstrip('/'), filename)
            save_image(image_file, path)
            data_dict['image_url'] = '%s://%s:%s/%s%s' % (
                request.url.scheme, request.url.host, request.url.port,
                settings.IMAGE_URL.lstrip('/'), filename)
        # data_dict.update({'dish_id':  get_next_sequence_value(counter_dish, 'dish_id')})
        try:
            dish = Dish(**data_dict)
            await dish.save()
        except InvalidOperation as e:
            return {'error': 'validation %s' % e}
        else:
            return {'message': 'Item successfully added'}

    @staticmethod
    def post_data_to_dict(data):
        _list_values = ('ingredients_en', 'ingredients_ru', 'tags')
        _int_values = ('cooking_time',)
        post_dict = dict()
        for key, value in data.items():
            if key in _list_values:
                new_value = [item.strip() for item in value.split(',')]
                value = new_value
            elif key in _int_values:
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    pass
            post_dict.update({key: value})
        return post_dict


class ShowAll(View):
    async def get(self):
        return await self.get_resp(self.request)

    @require('admin')
    @aiohttp_jinja2.template('show_all.html')
    async def get_resp(self, request):
        dish_list = await Dish.find()
        return {'dishes': dish_list}


class Logout(View):
    async def get(self):
        return await self.get_resp(self.request)

    @require('admin')
    async def get_resp(self, request):
        response = web.HTTPFound('/')
        await forget(request, response)
        return response

import aiohttp_jinja2
from aiohttp.web import View
from helper import save_image, ValidationError
import pymongo
import hashlib
import settings
from models import model

connection = pymongo.MongoClient('mongodb://localhost')
db = connection.breakfast
dishes = db.dishes

class Index(View):
    async def get(self):
        return await self.get_index(self.request)

    @aiohttp_jinja2.template('index.jinja2')
    async def get_index(self, request):
        return None


class CreateItem(View):

    async def get(self):
        return await self.get_resp(self.request)

    async def post(self):
        return await self.post_resp(self.request)

    @aiohttp_jinja2.template('create_item.jinja2')
    async def get_resp(self, request):
        return {'user': 'Toma', 'role': 'superuser'}

    @aiohttp_jinja2.template('create_item.jinja2')
    async def post_resp(self, request):
        data = await request.post()
        try:
            data_dict = self.post_data_to_dict(data)
        except ValidationError as e:
            return {'error': e}
        if data['image']:
            data_dict.pop('image')
            image = data['image']
            image_file = image.file
            filename = image.filename
            #filename = hashlib.sha1(bytearray(image.filename, 'utf8')).hexdigest()
            path = '%s/%s' % (settings.IMAGE_DIRECTORY.rstrip('/'), filename)
            save_image(image_file, path)
            data_dict['image_url'] = '%s://%s:%s/%s%s' % (
                request.url.scheme, request.url.host, request.url.port,
                settings.IMAGE_URL.lstrip('/'), filename)
        #Todo validate input
        dishes.insert(data_dict)

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
                    raise ValidationError(key)
            post_dict.update({key: value})
        return post_dict
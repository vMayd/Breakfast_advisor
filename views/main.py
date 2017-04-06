
import aiohttp_jinja2

from aiohttp import web
from aiohttp.web import View
from aiohttp_security import remember
from passlib.hash import sha256_crypt
from mongoengine.errors import SaveConditionError, ValidationError as MongoValidationError

import settings
from models.model import User, Permission, users, permission
from db_auth import check_credentials


class Index(View):
    async def get(self):
        return await self.get_index(self.request)

    @aiohttp_jinja2.template('index.html')
    async def get_index(self, request):
        return None


class Login(View):
    async def get(self):
        return await self.get_resp(self.request)

    async def post(self):
        return await self.handle_post(self.request)

    @aiohttp_jinja2.template('login.html')
    async def get_resp(self, request):
        return {'message': "Please log in"}

    @aiohttp_jinja2.template('login.html')
    async def handle_post(self, request):
        response = web.HTTPFound('/admin/')
        form = await request.post()
        login = form.get('username')
        password = form.get('password')
        if await check_credentials(login, password):
            await remember(request, response, login)
            user = await users.find_one({'login': login})
            response.set_cookie('bkAdv|usr', '%s|%s' % (login, user['name']), max_age=settings.COOKIE_AGE)
            return response

        return {'error': 'Wrong username or password'}


class Registration(View):
    async def get(self):
        return await self.handle_get(self.request)

    async def post(self):
        return await self.handle_post(self.request)

    @aiohttp_jinja2.template('registration.html')
    async def handle_get(self, request):
        return {'form': {}}

    @aiohttp_jinja2.template('registration.html')
    async def handle_post(self, request):
        form = await request.post()
        name = form.get('name')
        email = form.get('email')
        username = form.get('username')
        password = form.get('password')
        confirm_password = form.get('confirm')
        if password != confirm_password:
            return {
                'form': form_to_dict(form),
                'error': 'Password confirmation failed.'
            }
        user_exists = await User.find_one(login=username)
        if user_exists:
            return {
                'form': form_to_dict(form),
                'error': 'User with given username already exists. Please use another username.'
            }
        password_hash = sha256_crypt.encrypt(password)
        try:
            user = User(name=name, email=email, login=username, password=password_hash,
                        is_superuser=False, disabled=False)
            await user.save()
            await Permission(user=user.user_id, perm_name='user').save()
        except (MongoValidationError, SaveConditionError):
            # todo: log reason here
            return {
                'form': form_to_dict(form),
                'error': 'Registration failed. Please try again'
            }
        else:
            return {
                'form': {},
                'message': 'Registration complete. Please login to continue.'
            }


def form_to_dict(form):
    ret_dict = dict()
    for field, value in form.items():
        ret_dict.update({field: value})
    return ret_dict
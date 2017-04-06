import asyncio

from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import sha256_crypt

from models import model


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self):
        pass

    @asyncio.coroutine
    def authorized_userid(self, identity):
        auth_user = yield from model.User.find_one(login=identity, disabled={'$ne': True})
        if auth_user:
            return identity
        else:
            return None

    @asyncio.coroutine
    def permits(self, identity, permission, context=None):
        if not identity:
            return False

        auth_user = yield from model.User.find_one(login=identity, disabled={'$ne': True})
        if auth_user:
            if auth_user.is_superuser:
                return True

            perms = yield from model.Permission.find(user=auth_user._id)
            for record in perms:
                if record.perm_name == permission:
                    return True
        return False


@asyncio.coroutine
def check_credentials(username, password):
    user = yield from model.User.find_one(login=username)
    if user:
        hash_pass = user.password
        passed = sha256_crypt.verify(password, hash_pass)
        return passed
    return False



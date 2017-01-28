import settings
from aiohttp import web
from api import Handler
from views.admin import CreateItem, Index

handler = Handler()
routes = [
    ('*', '/', Index, 'index'),
    ('POST', '/api/recipe/', handler.recipe, 'recipe', web.Request.json),
    ('*', '/admin/add', CreateItem, 'create_item')
]


def setup_routes(app):
    for route in routes:
        if len(route) > 4:
            app.router.add_route(route[0], route[1], route[2], name=route[3], expect_handler=route[4])
        else:
            app.router.add_route(route[0], route[1], route[2], name=route[3])


def setup_static(app):
    app.router.add_static('/static/', path=str(settings.ROOT), name='static', follow_symlinks=True)
    # app.router.add_static('/static/style/', path=str(settings.ROOT + '/' + 'styles'), name='styles')

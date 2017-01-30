import settings
from aiohttp import web
from views.admin import CreateItem, Index, ShowAll
from api.api import Drinks, MainDish, FirstDish, SecondDish, DishApi

routes = [
    ('*', '/', Index, 'index'),
    ('*', '/api/dishes/', DishApi, 'recipe', web.Request.json),
    ('*', '/admin/add', CreateItem, 'create_item'),
    ('*', '/admin/items', ShowAll, 'show_all_items'),
    ('*', '/api/drink/', Drinks, 'api_drink'),
    ('*', '/api/dish/main/', MainDish, 'api_dish_main'),
    ('*', '/api/dish/first/', FirstDish, 'api_dish_first'),
    ('*', '/api/dish/second/', SecondDish, 'api_dish_second'),
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

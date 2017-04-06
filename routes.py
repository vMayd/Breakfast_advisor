import settings
from aiohttp import web
from views.admin import CreateItem, Users, ShowAll, Logout
from views.main import Index, Login, Registration
from api.api import Drinks, MainDish, FirstDish, SecondDish, DishApi

routes = {
    'admin': [
        ('*', '/add/', CreateItem, 'create_item'),
        ('*', '/', Users, 'users'),
        ('*', '/items/', ShowAll, 'show_all_items'),
    ],
    'main': [
        ('*', '/', Index, 'index'),
        ('*', '/login/', Login, 'login'),
        ('*', '/logout/', Logout, 'logout'),
        ('*', '/registration/', Registration, 'registration'),
    ],
    'api': [
        ('*', '/query/', DishApi, 'query'),
        ('*', '/drink/', Drinks, 'api_drink'),
        ('*', '/dish/main/', MainDish, 'api_dish_main'),
        ('*', '/dish/first/', FirstDish, 'api_dish_first'),
        ('*', '/dish/second/', SecondDish, 'api_dish_second'),
    ]
}


def setup_routes(app, name):
    assert name in routes.keys(), 'Make sure that provided name present in routes'
    for route in routes[name]:
        if len(route) > 4:
            app.router.add_route(route[0], route[1], route[2], name=route[3], expect_handler=route[4])
        else:
            app.router.add_route(route[0], route[1], route[2], name=route[3])


def setup_static(app):
    app.router.add_static('/static/', path=str(settings.ROOT), name='static', follow_symlinks=True)
    # app.router.add_static('/static/style/', path=str(settings.ROOT + '/' + 'styles'), name='styles')

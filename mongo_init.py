import pymongo
import random
import string
from models import helper
from models.model import counter_dish
# #
connection = pymongo.MongoClient('mongodb://localhost')
db = connection.breakfast
dishes = db.dishes
counter = db.counters

# dishes = Collection('breakfast', 'dishes')
categories = ['drink', 'main_dish', 'aux_dish']
tags = ['no fat', 'light', 'heavy', 'fried', 'steam']


def insert_query(n):
    insert = {
        'dish_id': helper.get_next_sequence_value(counter_dish, 'dish_id'),
        'name_en': 'Dish %s' % n,
        'name_ru': 'Блюдо %s' % n,
        'description_en': 'Perfect dish for %s person (persons)' % n,
        'description_ru': 'Отличное блюдо для %s человек' % n,
        'recipe_en': 'Mix all of %s ingredients. Its tasty' % n,
        'recipe_ru': 'Смешайте все %s ингредиента(-ов). Приятного...' % n,
        'ingredients_en': [string.ascii_lowercase[random.randrange(0, stop=i+1)] for i in range(n)],
        'ingredients_ru': [string.ascii_lowercase[random.randrange(0, stop=i+1)] for i in range(n)],
        'category': categories[random.randrange(start=0, stop=3)],
        'cooking_time': n,
        'image_url': 'http://localhost:8080/static/qw.png',
        'tags': [tags[random.randint(0, len(tags)-1)] for _ in range(random.randint(0, len(tags)-1))]
    }
    return insert

for n in range(20):
    dishes.insert_one(insert_query(n))

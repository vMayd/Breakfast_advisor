import jsonschema
from jsonschema import exceptions
from logger import *
from motor import motor_asyncio
from validator import dish as dish_schema
from mongoengine import *

# connection = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
client = motor_asyncio.AsyncIOMotorClient('localhost', 27017)
breakfast = client.breakfast

# dishes = breakfast.dishes
# counter = breakfast.counter
# counter_dish = breakfast.counter_dish
# users = breakfast.user
# permission = breakfast.permission


class MetaCollection(type):

    def __new__(mcs, name, bases, dct):
        cls = super(MetaCollection, mcs).__new__(mcs, name, bases, dct)
        if not getattr(cls, '_database', False):
            setattr(cls, '_database', 'test')
        if not getattr(cls, '_collection', False):
            setattr(cls, '_collection', 'test')
        collection = client[getattr(cls, '_database')][getattr(cls, '_collection')]
        counter = client[getattr(cls, '_database')]['counter']
        setattr(cls, 'collection', collection)
        setattr(cls, 'counter', counter)
        if not getattr(cls, 'schema', False):
            setattr(cls, 'schema', {})
        return cls


class BaseModel(metaclass=MetaCollection):

    def __init__(self, **kwargs):
        self._init_object(**kwargs)

    def __str__(self):
        return '{name} {id}'.format(name=self.__class__.__name__, id=self._id)

    def __repr__(self):
        return '{name} {args}'.format(name=self.__class__.__name__, args=self.__dict__)

    def _init_object(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        # if self.sequence_field:
        #     setattr(self, self.sequence_field, self.get_next_sequence_value())

    async def get_next_sequence_value(self):
        counter_name = self.__class__.__name__.lower()
        if not await self.counter.find_one({'_id': counter_name}):
            await self.counter.insert_one({'_id': counter_name, 'seq': 0})
        doc = await self.counter.find_one_and_update(
            {'_id': self.__class__.__name__.lower()},
            {'$inc': {'seq': 1}},
            return_document=True
        )
        return doc['seq']

    @classmethod
    async def find_one(cls, **kwargs):
        result = await cls.collection.find_one(kwargs)
        if result:
            return cls(**result)

    def validate(self):
        try:
            jsonschema.validate(self.__dict__, self.schema)
        except exceptions.ValidationError as e:
            server_logger.error(e)
            raise ValidationError(e)

    @classmethod
    async def find(cls, **query):
        cursor = cls.collection.find(query)
        result = await cursor.to_list(length=100)
        return [cls(**doc) for doc in result]

    @classmethod
    async def insert(cls, **fields):
        await cls.collection.insert_one(fields)

    async def save(self):
        self.validate()
        if self.sequence_field and self.sequence_field not in self.__dict__:
                seq_value = await self.get_next_sequence_value()
                setattr(self, self.sequence_field, seq_value)
        _filter = {self.sequence_field: getattr(self, self.sequence_field)}
        doc = await self.collection.find_one_and_replace(_filter, self.__dict__, upsert=True, return_document=True)
        self._init_object(**doc)

    @classmethod
    async def delete(cls, **query):
        await cls.collection.find_one_and_delete(query)


class User(BaseModel):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    _database = 'breakfast'
    _collection = 'user'
    sequence_field = 'user_id'


class Permission(BaseModel):

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)

    _database = 'breakfast'
    _collection = 'permission'
    sequence_field = 'permission_id'


class Dish(BaseModel):

    def __init__(self, **kwargs):
        super(Dish, self).__init__(**kwargs)

    _database = 'breakfast'
    _collection = 'dishes'
    sequence_field = 'dish_id'
    schema = dish_schema

    CATEGORIES = (
        ("drink", "Drink"),
        ("main_dish", "Main Dish"),
        ("second_1", "Second #1"),
        ("second_2", "Second #2"),
    )

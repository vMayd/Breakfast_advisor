import pymongo
import settings

connection = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)

breakfast = connection.breakfast

dishes = breakfast.dishes
counter = breakfast.counter
counter_dish = breakfast.counter_dish


# class BaseDb(pymongo.MongoClient):
#     def __init__(self, db, collection, *args, **kwargs):
#         super(BaseDb, self).__init__(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT, *args, **kwargs)
#         self.db = super(BaseDb, self).get_database(db)
#         self.collection = self.db.get_collection(collection)
#
#     def get_next_sequence_value(self, counter, sequence_name):
#         assert isinstance(counter, pymongo.collection.Collection), 'Counter must be of collection type'
#         doc = counter.find_one_and_update(
#             {'_id': sequence_name},
#             {'$inc': {'seq': 1}},
#             return_document=pymongo.ReturnDocument.AFTER
#             )
#         return doc['seq']
#
#     @classmethod
#     def parse_query_args(cls, query):
#         parsed_args = {}
#         for k, v in query.items():
#             if isinstance(v, dict):
#                 parsed_args.update({k: {'$' + v['query_op']: v['value']}})
#             else:
#                 parsed_args.update({k: v})
#         return parsed_args
#
#     def get_items(self, query_args):
#         query = self.parse_query_args(query_args)
#         result = self.collection.find(query).sort([('_id', pymongo.ASCENDING)])
#         dishes = [item for item in result]
#         return dishes
#
#
# class Collection(BaseDb):
#     def __init__(self, *args, **kwargs):
#         super(Collection, self).__init__(*args, **kwargs)
#
#     def insert_one(self, *args, **kwargs):
#         return self.collection.insert(*args, **kwargs)
#
#     def insert_many(self, *args, **kwargs):
#         return self.collection.insert_many(*args, **kwargs)
#
#     def find_one(self, *args, **kwargs):
#         return self.collection.find_one(*args, **kwargs)
#
#     def find(self, *args, **kwargs):
#         return self.collection.find(*args, **kwargs)






# todo: think about recursion
# def parse_query_args2(query, result_dict):
#     for k, v in query.items():
#         if isinstance(v, dict):
#             parse_query_args2(v, result_dict)
#         else:
#             result_dict.update({k: v})

# def insert(args):

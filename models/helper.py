import pymongo


def get_next_sequence_value(counter, sequence_name):
    assert isinstance(counter, pymongo.collection.Collection), 'Counter must be of collection type'
    if not counter.find_one():
        counter.insert_one({'_id': sequence_name, 'seq': 0})
    doc = counter.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'seq': 1}},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return doc['seq']


def parse_query_args(query):
    parsed_args = {}
    for k, v in query.items():
        if isinstance(v, dict):
            parsed_args.update({k: {'$' + v['query_op']: v['value']}})
        else:
            parsed_args.update({k: v})
    return parsed_args


def get_items(collection, query_args):
    query = parse_query_args(query_args)
    result = collection.find(query, {"_id": 0}).sort([('_id', pymongo.ASCENDING)])
    items = cursor_to_list(result)
    return items


def cursor_to_list(cursor_obj):
    return [item for item in cursor_obj]
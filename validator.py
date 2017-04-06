import jsonschema

api_schema_ = {
    "definitions": {
        "query_a": {
            "type": "object",
            "properties": {
                "query_op": {"type": "string", "enum": ["eq", "gt", "gte", "lt", "lte", "ne"]},
                "value": {"type": "number"}
            }
        },
        "query_b": {
            "type": "object",
            "properties": {
                "query_op": {"type": "string", "enum": ["in", "nin"]},
                "value": {"type": "array"}
            }
        },
    },
    "type": "object",
    "properties": {
        "dish_id": {"oneOf": [
            {"$ref": "#/definitions/query_a"},
            {"$ref": "#/definitions/query_b"},
            {"type": "number"}
        ]
        },
        "name_en": {"oneOf": [
            {"$ref": "#/definitions/query_b"},
            {"type": "string"}
        ]
        },
        "name_ru": {"oneOf": [
            {"$ref": "#/definitions/query_b"},
            {"type": "string"}
        ]
        },
        "ingredients_en": {"$ref": "#/definitions/query_b"},
        "ingredients_ru": {"$ref": "#/definitions/query_b"},
        "category": {"oneOf": [
            {"$ref": "#/definitions/query_b"},
            {"type": "string"}
        ]
        },
        "cooking_time": {"oneOf": [
            {"$ref": "#/definitions/query_a"},
            {"type": "number"}
        ]
        },
        "tags": {"oneOf": [
            {"$ref": "#/definitions/query_b"},
            {"type": "string"}
        ]
        }
    },
    "additionalProperties": False
}

dish = {
    "type": "object",
    "properties": {
        "name_en": {"type": "string"},
        "name_ru": {"type": "string"},
        "description_en": {"type": "string" },
        "description_ru": {"type": "string" },
        "recipe_en": {"type": "string"},
        "recipe_ru": {"type": "string"},
        "ingredients_en": {"type": "array"},
        "ingredients_ru": {"type": "array"},
        "category": {"type": "string"},
        "cooking_time": {"type": "number"},
        "tags": {"type": "array"},
        "image_url": {"type": "string"},
    },
    "required": ["name_en", "description_en", "ingredients_en", "category", "cooking_time", "image_url"],
    "additionalProperties": True

}

validators = {
    "query": api_schema_,
    "dish": dish,
}


def validate(url, arg_dict):
    return jsonschema.validate(arg_dict, schema=validators[url])
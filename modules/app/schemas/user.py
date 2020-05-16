from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    'type': 'object',
    'properties': {
        'user': {
            'type': 'string',
            'minLength': 4
        },
        'password': {
            'type': 'string',
            'minLength': 5
        },
        'role': {
            'type': 'string'
        },
        'active': {
            'type': 'boolean'
        }
    },
    'required': ['user', 'password'],
    'additionalProperties': False
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
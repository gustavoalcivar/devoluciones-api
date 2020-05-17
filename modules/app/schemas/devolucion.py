from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

devolucion_schema = {
    'type': 'object',
    'properties': {
        'ciudad': {
            'type': 'string',
            'minLength': 3
        },
        'local': {
            'type': 'string',
            'minLength': 3
        },
        'anio': {
            'type': 'integer',
            'minimum': 2010
        },
        'mes': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 12
        },
        'dia': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 31
        },
        'bandejas': {
            'type': 'number',
            'minimum': 1
        }
    },
    'required': ['ciudad', 'local', 'anio', 'mes', 'dia', 'bandejas'],
    'additionalProperties': False
}


def validate_devolucion(data):
    try:
        validate(data, devolucion_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
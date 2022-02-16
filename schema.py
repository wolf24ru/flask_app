NEW_THING = {
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
        },
        'user_name': {
            'type': 'string'
        },
        'password': {
            'type': 'string',
            'pattern': '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        },
    },
    'required': ['title', 'user_name', 'password']
}
NEW_USER = {
    'type': 'object',
    'properties': {
        'user_name': {
            'type': 'string'
        },
        'password': {
            'type': 'string',
            'pattern': '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        }
    },
    'required': ['user_name', 'password']
}

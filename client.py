import requests

URL = 'http://127.0.0.1:8000/'
# response = requests.get(f'{URL}health')
response = requests.post(f'{URL}user',
                         json={
                             'user_name': 'dsfsd f32',
                             'password': '12333Sdf545sdf'
                         })

print(response)
import requests
URL = 'http://127.0.0.1:8000/'

response = requests.get(f'{URL}health')

# create new user
# response = requests.post(f'{URL}new_user',
#                          json={
#                              'user_name': 'user_3',
#                              'password': '12333Sdf545sdf'
#                          })

# get user fo id
get_user = requests.get(f'{URL}get_use/1')
print(f'get_user: {get_user.json()}')

# create advertisement
create_advertisement = requests.post(f'{URL}adv_new',
                                     json={
                                         'title': 'thing_2',
                                         'description': 'lzlzl',
                                         'user_name': 'user_1',
                                         'password': '12333Sdf545sdf',
                                     })
print('____create_advertisement____')
print(create_advertisement)
print(create_advertisement.json())

get_advertisement_all = requests.get(f'{URL}adv_new')

get_advertisement_1 = requests.get(f'{URL}adv_new/1')

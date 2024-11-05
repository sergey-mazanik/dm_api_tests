import requests
from pprint import pprint
from json import loads


def test_post_v1_account():
    # Регистрация пользователя

    login = 'smazanik4'
    password = '123456'
    email = f'{login}@gmail.com'

    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f'User is not created! {response.json()}'

    # Получить письмо из почтового сервера

    params = {
        'limit': '100',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    assert response.status_code == 200, 'Email does not received!'

    # Получить активационный токен
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    assert token is not None, f'Token for user {login} does not received!'

    # Активация пользователя

    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}', headers=headers)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'User does not activated!'

    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', headers=headers, json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'User does not authorize!'

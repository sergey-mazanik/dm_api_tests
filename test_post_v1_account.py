import requests


def test_post_v1_account():
    # Регистрация пользователя
    login = 'smazanik'
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

    # Получить письмо из почтового сервера
    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)

    # Получить активационный токен
    ...
    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/83c7a049-5dc0-4031-b96d-adcc3f97fa4f', headers=headers)
    print(response.status_code)
    print(response.text)

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', headers=headers, json=json_data)
    print(response.status_code)
    print(response.text)

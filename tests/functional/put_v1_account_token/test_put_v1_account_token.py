from json import loads

from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_put_v1_account_token():
    # Регистрация пользователя
    account_api = AccountApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')
    login = 'smazanik30'
    password = '123456'
    email = f'{login}@gmail.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }
    response = account_api.post_v1_account(json_data=json_data)
    print_log(response=response)
    assert response.status_code == 201, f'User is not created! {response.json()}'

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    print_log_without_response_body(response=response)
    assert response.status_code == 200, 'Email does not received!'

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    print(token)
    assert token is not None, f'Token for user {login} does not received!'

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print_log(response=response)
    assert response.status_code == 200, 'User does not activated!'


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token


def print_log(response):
    log = f"""
    REQUEST:
        URL: {response.request.url}
        METHOD: {response.request.method}
        JSON:   {response.request.body}

    RESPONSE:    
        STATUS_CODE: {response.status_code}
        CONTENT: {response.content}
    """
    print(log)


def print_log_without_response_body(response):
    log = f"""
        REQUEST:
            URL: {response.request.url}
            METHOD: {response.request.method}
            JSON:   {response.request.body}

        RESPONSE:    
            STATUS_CODE: {response.status_code}
        """
    print(log)

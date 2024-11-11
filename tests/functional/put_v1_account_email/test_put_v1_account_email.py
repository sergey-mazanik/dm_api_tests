from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)


def test_put_v1_account_email():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(
        host='http://5.63.153.31:5025'
        )
    dm_api_configuration = DmApiConfiguration(
        host='http://5.63.153.31:5051',
        disable_log=False
        )
    account_api = AccountApi(
        configuration=dm_api_configuration
    )
    login_api = LoginApi(
        configuration=dm_api_configuration
    )
    mailhog_api = MailhogApi(
        configuration=mailhog_configuration
    )
    login = 'smazanik60'
    password = '123456'
    email = f'{login}@gmail.com'
    new_email = f'{login}+1@gmail.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }
    response = account_api.post_v1_account(
        json_data=json_data
    )
    assert response.status_code == 201, f'User is not created! {response.json()}'

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, 'Email does not received!'

    # Получить активационный токен
    token = get_activation_token_by_login(
        login,
        response
    )
    print(
        token
    )
    assert token is not None, f'Token for user {login} does not received!'

    # Активация пользователя
    response = account_api.put_v1_account_token(
        token=token
    )
    assert response.status_code == 200, 'User does not activated!'

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(
        json_data=json_data
    )
    assert response.status_code == 200, 'User does not authorize!'

    # Получить токен авторизации
    auth_token = response.headers['X-Dm-Auth-Token']

    # Изменить емейл
    json_data = {
        "login": login,
        "password": password,
        "email": new_email
    }
    response = account_api.put_v1_account_email(
        json_data=json_data
    )
    assert response.status_code == 200, 'Email does not change!'

    # Разлогинится
    headers = {
        'X-Dm-Auth-Token': auth_token
    }
    response = login_api.delete_v1_account_login(
        headers=headers
    )
    assert response.status_code == 204, 'User is not unauthorized!'

    # Авторизоваться (ожидаем 403)
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(
        json_data=json_data
    )
    assert response.status_code == 403, 'Here should be an error!'

    # Получить письма из почтового сервиса
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, 'Email does not received!'

    # Получить токен для смены емейла
    token = get_activation_token_by_login(
        login,
        response
    )
    print(
        token
    )
    assert token is not None, f'Token for user {login} does not received!'

    # Активировать токен
    response = account_api.put_v1_account_token(
        token=token
    )
    assert response.status_code == 200, 'User does not activated!'

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }
    response = login_api.post_v1_account_login(
        json_data=json_data
    )
    assert response.status_code == 200, 'Here should be an error!'


def get_activation_token_by_login(
        login,
        response
        ):
    token = None
    for item in response.json()['items']:
        user_data = loads(
            item['Content']['Body']
        )
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split(
                '/'
            )[-1]
    return token

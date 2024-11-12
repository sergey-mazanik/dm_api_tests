from json import loads

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount


class AccountHelper:

    auth_token = None

    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(
            self,
            login: str,
            email: str,
            password: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }

        response = self.dm_account_api.account_api.post_v1_account(
            json_data=json_data
        )
        assert response.status_code == 201, f'User is not created! {response.json()}'
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            expected_status_code: int = 200
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data=json_data
        )
        assert response.status_code == expected_status_code, 'User does not authorize!'
        return response

    def get_auth_token(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data=json_data
        )
        assert response.status_code == 200, 'User does not authorize!'
        AccountHelper.auth_token = self.get_auth_token_from_headers(
            response
        )
        return AccountHelper.auth_token

    def logout_current_user(
            self,
            auth_token
    ):
        headers = {
            'X-Dm-Auth-Token': auth_token
        }
        response = self.dm_account_api.login_api.delete_v1_account_login(
            headers=headers
        )
        assert response.status_code == 204, 'User is not unauthorized!'

    def change_email(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            "login": login,
            "password": password,
            "email": email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(
            json_data=json_data
        )
        assert response.status_code == 200, 'Email does not change!'

    def activate_user(
            self,
            login: str
    ):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, 'Email does not received!'

        token = self.get_activation_token_by_login(
            login=login,
            response=response
        )
        assert token is not None, f'Token for user {login} does not received!'

        response = self.dm_account_api.account_api.put_v1_account_token(
            token=token
        )
        assert response.status_code == 200, 'User does not activated!'
        return response

    @staticmethod
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

    @staticmethod
    def get_auth_token_from_headers(
            response
    ):
        auth_token = response.headers['X-Dm-Auth-Token']
        assert auth_token is not None
        return auth_token
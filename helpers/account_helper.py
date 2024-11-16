import time
from json import loads
from retrying import retry

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            print(
                f'Attempt number - {count + 1}'
            )
            token = function(
                *args,
                **kwargs
            )
            count += 1
            if count == 5:
                raise AssertionError(
                    'Too many retries to get activation token'
                )
            if token:
                return token
            time.sleep(
                0.5
            )

    return wrapper


class AccountHelper:
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

    def activate_user(
            self,
            token: str
    ):
        response = self.dm_account_api.account_api.put_v1_account_token(
            token=token
        )
        assert response.status_code == 200, 'User does not activated!'
        return response

    def register_and_activate_user(
            self,
            login: str,
            email: str,
            password: str
    ):
        self.register_new_user(
            login=login,
            email=email,
            password=password
        )
        token = self.get_activation_token_by_login(
            login=login
        )
        self.activate_user(
            token=token
        )

    def find_activation_mail_and_activate_user(
            self,
            login: str
    ):
        token = self.get_activation_token_by_login(
            login=login
        )
        assert token is not None, f'Token for user {login} does not received!'
        self.activate_user(
            token=token
        )

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

    def logout_current_user(
            self,
            **kwargs
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login(**kwargs)
        assert response.status_code == 204, 'User is not unauthorized!'

    def logout_user_from_all_devices(
            self,
            **kwargs
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login_all(**kwargs)
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

    # @retrier
    @retry(
        stop_max_attempt_number=5,
        retry_on_result=retry_if_result_none,
        wait_fixed=1000
    )
    def get_activation_token_by_login(
            self,
            login: str,
            token_type: str = 'activate'
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(
                item['Content']['Body']
            )
            user_login = user_data['Login']
            if user_login == login and token_type == 'activate' and user_data.get(
                    'ConfirmationLinkUrl'
            ):
                token = user_data['ConfirmationLinkUrl'].split(
                    '/'
                )[-1]
            elif user_login == login and token_type == 'reset' and user_data.get(
                    'ConfirmationLinkUri'
            ):
                token = user_data['ConfirmationLinkUri'].split(
                    '/'
                )[-1]
        return token

    def auth_client(
            self,
            login: str,
            password: str
    ):
        json_data = {
            'login': login,
            'password': password
        }
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data=json_data
        )
        auth_token = response.headers['X-Dm-Auth-Token']
        auth_token_header = {
            'X-Dm-Auth-Token': auth_token
        }
        self.dm_account_api.account_api.set_headers(
            auth_token_header
        )
        self.dm_account_api.login_api.set_headers(
            auth_token_header
        )

    def reset_password(
            self,
            login: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email
        }
        response = self.dm_account_api.account_api.post_v1_account_password(
            json_data=json_data
        )
        return response

    def change_password(
            self,
            login: str,
            token: str,
            old_password: str,
            new_password: str
    ):
        json_data = {
            "login": login,
            "token": token,
            "oldPassword": old_password,
            "newPassword": new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(
            json_data=json_data
        )
        return response

    def reset_and_change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        self.reset_password(
            login=login,
            email=email
        )
        token = self.get_activation_token_by_login(
            login=login,
            token_type='reset'
        )
        self.change_password(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
        )

    def get_user_info(self):
        self.dm_account_api.account_api.get_v1_account()

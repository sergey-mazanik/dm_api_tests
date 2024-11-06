import requests

from main import response


class LoginApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.headers = headers

    def post_v1_account_login(
            self,
            json_data
    ):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account/login',
            json=json_data
        )
        return response

    def delete_v1_account_login(
            self,
            headers
    ):
        """
         Logout as current user
        :param headers:
        :return:
        """
        response = requests.delete(
            url=f'{self.host}/v1/account/login',
            headers=headers
        )
        return response

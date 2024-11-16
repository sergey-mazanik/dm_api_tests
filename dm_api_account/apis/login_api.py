import requests


from restclient.client import RestClient


class LoginApi(
    RestClient
    ):

    def post_v1_account_login(
            self,
            json_data
    ):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """

        response = self.post(
            path=f'/v1/account/login',
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

        response = self.delete(
            path=f'/v1/account/login',
            headers=headers
        )
        return response

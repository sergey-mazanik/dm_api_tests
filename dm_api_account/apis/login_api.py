import allure
import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(
    RestClient
):

    @allure.step('Authenticate via credentials')
    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            validate_response=True
    ):
        """
        Authenticate via credentials
        :return:
        """
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(
                exclude_none=True,
                by_alias=True
            )
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Logout as current user')
    def delete_v1_account_login(
            self,
            **kwargs
    ):
        """
         Logout as current user
        :param kwargs:
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login',
            **kwargs
        )
        return response

    @allure.step('Logout from every device')
    def delete_v1_account_login_all(
            self,
            **kwargs
    ):
        """
        Logout from every device
        :param kwargs:
        :return:
        """
        response = self.delete(
            path='/v1/account/login/all',
            **kwargs
        )
        return response

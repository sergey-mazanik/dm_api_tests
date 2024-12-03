import allure
import requests

from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from clients.http.dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


class AccountApi(
    RestClient
):

    @allure.step('Register new user')
    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        Register new user
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(
                exclude_none=True,
                by_alias=True
            )
        )
        return response

    @allure.step('Activate registered user')
    def put_v1_account_token(
            self,
            token,
            validate_response=True
    ):
        """
        Activate registered user
        :param token:
        :param validate_response:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
            return UserEnvelope(
                **response.json()
            )
        return response

    @allure.step('Change registered user email')
    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response=True
    ):
        """
        Change registered user email
        :return:
        """
        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(
                exclude_none=True,
                by_alias=True
            )
        )
        if validate_response:
            return UserEnvelope(
                **response.json()
            )
        return response

    @allure.step('Get current user')
    def get_v1_account(
            self,
            validate_response=True,
            **kwargs
    ):
        """
        Get current user
        :return:
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(
                **response.json()
            )
        return response

    @allure.step('Change registered user password')
    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response=True
    ):
        """
        Change registered user password
        :return:
        """
        response = self.put(
            path='/v1/account/password',
            json=change_password.model_dump(
                exclude_none=True,
                by_alias=True
            )
        )
        if validate_response:
            return UserEnvelope(
                **response.json()
            )
        return response

    @allure.step('Reset registered user password')
    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response=True
    ):
        """
        Reset registered user password
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(
                exclude_none=True,
                by_alias=True
            )
        )
        if validate_response:
            return UserEnvelope(
                **response.json()
            )
        return response

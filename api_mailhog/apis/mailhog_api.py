import allure
import requests


from restclient.client import RestClient


class MailhogApi(
    RestClient
    ):

    @allure.step('Get users emails')
    def get_api_v2_messages(
            self,
            limit='2'
    ):
        """
        Get users emails
        :return:
        """
        params = {
            'limit': limit,
        }

        response = self.get(
            path=f'/api/v2/messages',
            params=params,
            verify=False
        )
        return response

import allure

from checkers.http_checkers import check_status_code_http
from checkers.get_v1_account import GetV1Account


@allure.parent_suite('Functional tests')
@allure.suite('Tests for method GET v1/account/auth')
@allure.sub_suite('Positive tests')
class TestGetV1AccountAuth:
    @allure.title('Check get current user')
    def test_get_v1_account_auth(
            self,
            auth_account_helper
    ):

        response = auth_account_helper.get_user_info(validate_response=True)

        GetV1Account.check_response_by_hamcrest(response)
        GetV1Account.check_response_by_assertpy(response)

    @allure.title('Check get current user without authentication')
    def test_get_v1_account_no_auth(
            self,
            account_helper
    ):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.get_user_info()

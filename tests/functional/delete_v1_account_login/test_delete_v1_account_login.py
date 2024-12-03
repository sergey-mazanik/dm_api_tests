import allure

from checkers.delete_v1_account_login import DeleteV1AccountLogin
from checkers.http_checkers import check_status_code_http

@allure.parent_suite('Functional tests')
@allure.suite('Tests for method DELETE v1/account/login')
@allure.sub_suite('Positive tests')
class TestDeleteV1AccountLogin:
    @allure.title('Check logout as current user')
    def test_delete_v1_account_login(
            self,
            account_helper,
            prepare_user,
            auth_account_helper
    ):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        account_helper.register_and_activate_user(
            login=login,
            email=email,
            password=password
        )

        account_helper.auth_client(
            login=login,
            password=password
        )

        with check_status_code_http(expected_status_code=204):
            response = account_helper.logout_current_user()

        DeleteV1AccountLogin.check_response_by_assertpy(response)

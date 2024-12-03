import allure

from checkers.post_v1_account_login import PostV1AccountLogin


@allure.parent_suite('Functional tests')
@allure.suite('Tests for method POST v1/account/login')
@allure.sub_suite('Positive tests')
class TestsPostV1AccountLogin:
    @allure.title('Check registration new user')
    def test_post_v1_account_login(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        account_helper.register_and_activate_user(
            login=login,
            email=email,
            password=password
        )

        response = account_helper.user_login(
            login=login,
            password=password,
            validate_response=True
        )

        PostV1AccountLogin.check_response_values(response)

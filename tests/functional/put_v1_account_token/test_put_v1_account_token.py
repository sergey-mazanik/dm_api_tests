import allure


@allure.parent_suite('Functional tests')
@allure.suite('Tests for method PUT v1/account/token')
@allure.sub_suite('Positive tests')
class TestPutV1AccountToken:
    @allure.title('Check activate registered user')
    def test_put_v1_account_token(
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

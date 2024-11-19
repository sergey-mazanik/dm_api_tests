from checkers.delete_v1_account_login import DeleteV1AccountLogin


def test_delete_v1_account_login(
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

    response = account_helper.logout_current_user()

    DeleteV1AccountLogin.check_response_by_assertpy(response)

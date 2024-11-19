from checkers.post_v1_account_login import PostV1AccountLogin


def test_post_v1_account_login(
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

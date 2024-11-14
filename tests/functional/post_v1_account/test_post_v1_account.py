def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )

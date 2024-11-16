def test_put_v1_account_email(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_email = prepare_user.new_email

    account_helper.register_and_activate_user(
        login=login,
        email=email,
        password=password
    )

    account_helper.auth_client(
        login=login,
        password=password
    )

    account_helper.change_email(
        login=login,
        password=password,
        email=new_email
    )

    account_helper.user_login(
        login=login,
        password=password,
        expected_status_code=403
    )

    account_helper.find_activation_mail_and_activate_user(
        login=login
    )

    account_helper.user_login(
        login=login,
        password=password
    )

from assertpy import assert_that, soft_assertions


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
    print(response)
    with soft_assertions():
        assert_that(response.status_code).is_equal_to(204)
        assert_that(response.request.headers).contains_key('X-Dm-Auth-Token')

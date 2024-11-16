import structlog
from helpers.account_helper import AccountHelper
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)


def test_put_v1_account_email():
    mailhog_configuration = MailhogConfiguration(
        host='http://5.63.153.31:5025'
    )
    dm_api_configuration = DmApiConfiguration(
        host='http://5.63.153.31:5051',
        disable_log=False
    )
    account = DMApiAccount(
        configuration=dm_api_configuration
    )
    mailhog = MailHogApi(
        configuration=mailhog_configuration
    )

    account_helper = AccountHelper(
        dm_account_api=account,
        mailhog=mailhog
    )

    login = 'smazanik157'
    password = '123456'
    email = f'{login}@gmail.com'
    new_email = f'{login}+1@gmail.com'

    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )

    account_helper.activate_user(
        login=login
    )

    account_helper.get_auth_token(
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

    account_helper.activate_user(
        login=login
    )

    account_helper.user_login(
        login=login,
        password=password
    )

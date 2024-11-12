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


def test_delete_v1_account_login():
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

    login = 'smazanik155'
    password = '123456'
    email = f'{login}@gmail.com'

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

    account_helper.logout_current_user(
        auth_token=AccountHelper.auth_token
    )

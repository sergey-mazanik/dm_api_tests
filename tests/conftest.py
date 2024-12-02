import os
from collections import namedtuple
from datetime import datetime

import pytest
import structlog
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v
from pathlib import Path
from helpers.account_helper import AccountHelper
from packages.notifier.bot import send_file
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from packages.restclient.configuration import Configuration as MailhogConfiguration
from packages.restclient.configuration import Configuration as DmApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
    'telegram.token',
    'telegram.chat_id',
)

@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host=v.get('service.dm_api_account'))
    reporter.setup("/swagger/Account/swagger.json")
    yield
    reporter.generate_report()
    reporter.cleanup_input_files()
    # send_file()

@pytest.fixture(scope='session', autouse=True)
def set_config(request):
    config = Path(__file__).joinpath('../../').joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f'{option}', request.config.getoption(f'--{option}'))
    os.environ['TELEGRAM_BOT_CHAT_ID'] = v.get('telegram.chat_id')
    os.environ['TELEGRAM_BOT_ACCESS_TOKEN'] = v.get('telegram.token')
    request.config.stash['telegram-notifier-addfields']['environment'] = config_name
    request.config.stash['telegram-notifier-addfields']['report'] = 'https://sergey-mazanik.github.io/dm_api_tests/'

def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='stg', help='run stg')

    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)

@pytest.fixture()
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(
        host=v.get('service.mailhog')
    )
    mailhog_client = MailHogApi(
        configuration=mailhog_configuration
    )
    return mailhog_client


@pytest.fixture()
def account_api():
    dm_api_configuration = DmApiConfiguration(
        host=v.get('service.dm_api_account'),
        disable_log=False
    )
    account = DMApiAccount(
        configuration=dm_api_configuration
    )
    return account


@pytest.fixture()
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(
        dm_account_api=account_api,
        mailhog=mailhog_api
    )
    return account_helper


@pytest.fixture()
def auth_account_helper(
        mailhog_api
):
    dm_api_configuration = DmApiConfiguration(
        host=v.get('service.dm_api_account'),
        disable_log=False
    )
    account = DMApiAccount(
        configuration=dm_api_configuration
    )

    account_helper = AccountHelper(
        dm_account_api=account,
        mailhog=mailhog_api
    )
    account_helper.auth_client(
        login=v.get('user.login'),
        password=v.get('user.password')
    )
    return account_helper


@pytest.fixture()
def prepare_user():
    now = datetime.now()
    data = now.strftime(
        "%d_%m_%Y_%H_%M_%S_%f"
    )
    login = f'smazanik{data}'
    password = v.get('user.password')
    new_password = f'{password}7'
    email = f'{login}@gmail.com'
    new_email = f'{login}+1@gmail.com'
    User = namedtuple(
        'User',
        ['login', 'password', 'email', 'new_email', 'new_password']
    )
    user = User(
        login=login,
        email=email,
        password=password,
        new_email=new_email,
        new_password=new_password
    )
    return user

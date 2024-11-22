from contextlib import contextmanager

import requests
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
        expected_status_code: requests.codes = requests.codes.OK,
        expected_message: str = ''
):
    try:
        yield
        if not 200 <= expected_status_code <= 299:
            raise AssertionError(f'Expected status code should be {expected_status_code}')
        if expected_message:
            raise AssertionError(f"Should be getting message '{expected_message}', but request is OK")
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()['title'] == expected_message

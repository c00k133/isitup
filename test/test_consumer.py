import pytest
from requests_mock import Mocker


@pytest.fixture()
def mock_ping():
    with Mocker() as mocker:
        mocker.register_uri(
            'GET',
            'http://domain1.com',
            [
                {'text': 'Domain1', 'status_code': 200},
                {'text': 'Not found', 'status_code': 404},
            ]
        )

        yield mocker

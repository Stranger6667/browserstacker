# coding: utf-8
import pytest

from browserstacker.screenshots import ScreenShotsAPI

from ._compat import patch, Mock


@pytest.fixture
def mocked_request(request):
    mock = patch('requests.request', Mock())
    mock.start()
    request.addfinalizer(mock.stop)
    return mock.new


@pytest.fixture(scope='session')
def screenshots_api():
    return ScreenShotsAPI(None, None)

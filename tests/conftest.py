# coding: utf-8
import os

import pytest

from browserstacker.screenshots import ScreenShotsAPI

from ._compat import builtins, mock_open, patch, Mock


def _make_mock(request, name, return_value):
    mock = patch(name, return_value)
    mock.start()
    request.addfinalizer(mock.stop)
    return mock.new


@pytest.fixture
def mocked_request(request):
    return _make_mock(request, 'requests.Session.request', Mock())


@pytest.fixture
def mocked_get(request):
    return _make_mock(request, 'browserstacker.screenshots.requests.Session.get', Mock())


@pytest.fixture
def list_browsers_response(mocked_request):
    mocked_request().json.return_value = LIST_BROWSERS_RESPONSE
    return mocked_request


@pytest.fixture(scope='session')
def screenshots_api():
    return ScreenShotsAPI(None, None)


@pytest.fixture
def mocked_image_response():

    class MockedContent:
        content = b'test'

        def iter_content(self, chunk_size=1024):
            for chunk in (self.content, None):
                yield chunk

    return MockedContent()


@pytest.fixture
def test_dir_name(request):
    directory_name = 'test_dir'

    def clean():
        try:
            os.rmdir(directory_name)
        except:
            pass

    request.addfinalizer(clean)
    return directory_name


@pytest.fixture
def mocked_open(request):
    mock = patch.object(builtins, 'open', mock_open())
    mock.start()
    request.addfinalizer(mock.stop)
    return mock.new


IMAGE_URL = 'http://www.example/screenshots/test_save.jpg'

LIST_BROWSERS_RESPONSE = [
    {'os': 'Windows', 'browser': 'safari', 'os_version': '8', 'browser_version': '5.1', 'device': None},
    {'os': 'Windows', 'browser': 'firefox', 'os_version': '7', 'browser_version': '30.0', 'device': None},
    {'os': 'OS X', 'browser': 'chrome', 'os_version': 'Lion', 'browser_version': '17.0', 'device': None},
    {'os': 'OS X', 'browser': 'firefox', 'os_version': 'Lion', 'browser_version': '18.0', 'device': None},
    {'os': 'ios', 'browser': 'Mobile Safari', 'os_version': '5.0', 'browser_version': None, 'device': 'iPad 2 (5.0)'},
    {'os': 'ios', 'browser': 'Mobile Safari', 'os_version': '7.0', 'browser_version': None, 'device': 'iPad Mini'},
    {'os': 'android', 'browser': 'Android Browser', 'os_version': '2.2', 'browser_version': None, 'device': 'HTC Wildfire'}
]

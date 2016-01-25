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
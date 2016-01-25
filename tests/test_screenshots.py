# coding: utf-8
import os

import pytest

from browserstacker import ScreenShotsAPI
from ._compat import patch


IMAGE_URL = 'http://www.example/screenshots/test_save.jpg'


def test_execute(screenshots_api, mocked_request):
    screenshots_api.execute('GET', 'test')
    mocked_request.assert_called_with(
        'GET',
        'https://www.browserstack.com/test',
        auth=screenshots_api.auth
    )


def test_list_browsers(screenshots_api, mocked_request):
    screenshots_api.list_browsers()
    mocked_request.assert_called_with(
        'GET',
        'https://www.browserstack.com/screenshots/browsers.json',
        auth=screenshots_api.auth
    )


def test_make_screenshots(screenshots_api, mocked_request, mocked_get, mocked_image_response, test_dir_name, mocked_open):
    url = 'http://www.example.com'
    mocked_request().json.return_value = {
        'job_id': '123',
        'screenshots': [
            {'image_url': 'http://www.example.com/img/test_image.jpg'}
        ]
    }
    mocked_get.return_value = mocked_image_response

    screenshots_api.make_screenshots(url, [{}], destination=test_dir_name)

    mocked_request._mock_mock_calls[1].assert_called_with(
        'POST',
        'https://www.browserstack.com/screenshots',
        auth=screenshots_api.auth,
        json={'url': url, 'browsers': [{}]}
    )
    # `open` args
    assert mocked_open._mock_mock_calls[0][1] == (os.path.join(test_dir_name, 'test_image.jpg'), 'wb')
    # `fd.write` args
    assert mocked_open._mock_mock_calls[2][1] == (mocked_image_response.content, )
    assert os.path.exists(test_dir_name)


@pytest.mark.parametrize(
    'browsers, resulting_browsers',
    (
        (None, [ScreenShotsAPI.default_browser]),
        ({}, [{}]),
        ([{}], [{}]),
    )
)
def test_generate_screenshots(screenshots_api, mocked_request, browsers, resulting_browsers):
    url = 'http://www.example.com'
    screenshots_api.generate_screenshots(url, browsers)
    mocked_request.assert_called_with(
        'POST',
        'https://www.browserstack.com/screenshots',
        auth=screenshots_api.auth,
        json={'url': url, 'browsers': resulting_browsers}
    )


def test_list_screenshots(screenshots_api, mocked_request):
    job_id = 'be9989892cbba9b9edc2c95f403050aa4996ac6a'
    screenshots_api.list_screenshots(job_id)
    mocked_request.assert_called_with(
        'GET',
        'https://www.browserstack.com/screenshots/%s.json' % job_id,
        auth=screenshots_api.auth
    )


def test_save_file(screenshots_api, mocked_open, mocked_image_response):
    filename = 'test.jpg'
    screenshots_api.save_file(filename, mocked_image_response)
    # `open` args
    assert mocked_open._mock_mock_calls[0][1] == (filename, 'wb')
    # `fd.write` args
    assert mocked_open._mock_mock_calls[2][1] == (mocked_image_response.content, )


def test_ensure_dir_not_exists(screenshots_api, test_dir_name):
    assert not os.path.exists(test_dir_name)
    screenshots_api.ensure_dir(test_dir_name)
    assert os.path.exists(test_dir_name)


def test_ensure_dir_exists(screenshots_api, test_dir_name):
    os.makedirs(test_dir_name)
    screenshots_api.ensure_dir(test_dir_name)
    assert os.path.exists(test_dir_name)


def test_ensure_dir_none(screenshots_api, test_dir_name):
    with patch('browserstacker.screenshots.os.makedirs') as makedirs:
        screenshots_api.ensure_dir(None)
        assert not makedirs.called


@pytest.mark.parametrize(
    'destination, filename',
    (
        (None, 'test_save.jpg'),
        ('test_dir', 'test_dir/test_save.jpg')
    )
)
def test_save_screenshot(screenshots_api, mocked_get, mocked_open, mocked_image_response, destination, filename):
    mocked_get.return_value = mocked_image_response
    screenshots_api.save_screenshot(IMAGE_URL, destination)
    # `open` args
    assert mocked_open._mock_mock_calls[0][1] == (filename, 'wb')
    # `fd.write` args
    assert mocked_open._mock_mock_calls[2][1] == (mocked_image_response.content, )


def test_download_screenshots(screenshots_api, test_dir_name, mocked_get, mocked_open, mocked_image_response):
    mocked_get.return_value = mocked_image_response
    with patch.object(screenshots_api, 'list_screenshots') as list_screenshots:
        list_screenshots.return_value = {'screenshots': [{'image_url': IMAGE_URL}]}
        screenshots_api.download_screenshots('123', test_dir_name)
    # `open` args
    assert mocked_open._mock_mock_calls[0][1] == (os.path.join(test_dir_name, 'test_save.jpg'), 'wb')
    # `fd.write` args
    assert mocked_open._mock_mock_calls[2][1] == (mocked_image_response.content, )
    assert os.path.exists(test_dir_name)

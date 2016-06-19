# coding: utf-8
import os

import pytest

from browserstacker import ScreenShotsAPI
from ._compat import patch
from .conftest import IMAGE_URL


def test_execute(screenshots_api, mocked_request):
    screenshots_api.execute('GET', 'test')
    mocked_request.assert_called_with(
        'GET',
        'https://www.browserstack.com/test',
        auth=screenshots_api.auth
    )


def test_browsers(screenshots_api, browsers_response):
    screenshots_api.browsers()
    browsers_response.assert_called_with(
        'GET',
        'https://www.browserstack.com/screenshots/browsers.json',
        auth=screenshots_api.auth
    )


parametrize_filtration = pytest.mark.parametrize(
    'filters, expected',
    (
        (
            {'os': 'Windows'},
            [
                {'os': 'Windows', 'browser': 'safari', 'os_version': '8', 'browser_version': '5.1', 'device': None},
                {'os': 'Windows', 'browser': 'firefox', 'os_version': '7', 'browser_version': '30.0', 'device': None}
            ],
        ),
        (
            {'browser': 'firefox', 'os_version': 'Lion'},
            [
                {'os': 'OS X', 'browser': 'firefox', 'os_version': 'Lion', 'browser_version': '18.0', 'device': None},
            ]
        ),
        (
            {'browser_version': 17.0},
            [
                {'os': 'OS X', 'browser': 'chrome', 'os_version': 'Lion', 'browser_version': '17.0', 'device': None},
            ]
        ),
        (
            {'os': ['android', 'ios']},
            [
                {'os': 'ios', 'browser': 'Mobile Safari', 'os_version': '5.0', 'browser_version': None, 'device': 'iPad 2 (5.0)'},
                {'os': 'ios', 'browser': 'Mobile Safari', 'os_version': '7.0', 'browser_version': None, 'device': 'iPad Mini'},
                {'os': 'android', 'browser': 'Android Browser', 'os_version': '2.2', 'browser_version': None, 'device': 'HTC Wildfire'}
            ]
        ),
    )
)


@parametrize_filtration
def test_browsers_filtration(screenshots_api, browsers_response, filters, expected):
    assert screenshots_api.browsers(**filters) == expected


@parametrize_filtration
def test_browsers_filtration_lowercase(screenshots_api, browsers_response, filters, expected):
    filters = dict((key, value.lower() if isinstance(value, str) else value) for key, value in filters.items())
    assert screenshots_api.browsers(**filters) == expected


def test_make(screenshots_api, mocked_request, mocked_get, mocked_image_response, test_dir_name, mocked_open):
    url = 'http://www.example.com'
    mocked_request().json.return_value = {
        'job_id': '123',
        'screenshots': [
            {'image_url': 'http://www.example.com/img/test_image.jpg', 'state': 'done'}
        ]
    }
    mocked_get.return_value = mocked_image_response

    screenshots_api.make(url, [{}], destination=test_dir_name)

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
def test_generate(screenshots_api, mocked_request, browsers, resulting_browsers):
    url = 'http://www.example.com'
    screenshots_api.generate(url, browsers)
    mocked_request.assert_called_with(
        'POST',
        'https://www.browserstack.com/screenshots',
        auth=screenshots_api.auth,
        json={'url': url, 'browsers': resulting_browsers}
    )


def test_list(screenshots_api, mocked_request):
    job_id = 'be9989892cbba9b9edc2c95f403050aa4996ac6a'
    screenshots_api.list(job_id)
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


@pytest.mark.parametrize(
    'destination, filename',
    (
        (None, 'test_save.jpg'),
        ('test_dir', 'test_dir/test_save.jpg')
    )
)
def test_save(screenshots_api, mocked_get, mocked_open, mocked_image_response, destination, filename):
    mocked_get.return_value = mocked_image_response
    screenshots_api.save(IMAGE_URL, destination)
    # `open` args
    assert mocked_open._mock_mock_calls[0][1] == (filename, 'wb')
    # `fd.write` args
    assert mocked_open._mock_mock_calls[2][1] == (mocked_image_response.content, )


def test_download(screenshots_api, test_dir_name, mocked_get, mocked_open, mocked_image_response):
    mocked_get.return_value = mocked_image_response
    with patch.object(screenshots_api, 'list') as list:
        list.return_value = {'screenshots': [{'image_url': IMAGE_URL, 'state': 'done'}]}
        screenshots_api.download('123', test_dir_name)
    # `open` args
    assert mocked_open._mock_mock_calls[0][1] == (os.path.join(test_dir_name, 'test_save.jpg'), 'wb')
    # `fd.write` args
    assert mocked_open._mock_mock_calls[2][1] == (mocked_image_response.content, )
    assert os.path.exists(test_dir_name)

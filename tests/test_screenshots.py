# coding: utf-8
import pytest


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


@pytest.mark.parametrize('browsers', ([{}], {}))
def test_generate_screenshots(screenshots_api, mocked_request, browsers):
    url = 'http://www.example.com'
    screenshots_api.generate_screenshots(url, browsers)
    mocked_request.assert_called_with(
        'POST',
        'https://www.browserstack.com/screenshots',
        auth=screenshots_api.auth,
        json={'url': url, 'browsers': [{}]}
    )


def test_list_screenshots(screenshots_api, mocked_request):
    job_id = 'be9989892cbba9b9edc2c95f403050aa4996ac6a'
    screenshots_api.list_screenshots(job_id)
    mocked_request.assert_called_with(
        'GET',
        'https://www.browserstack.com/screenshots/%s.json' % job_id,
        auth=screenshots_api.auth
    )

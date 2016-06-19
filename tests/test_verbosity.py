# coding: utf-8
import pytest

from browserstacker import ScreenShotsAPI
from ._compat import patch
from .conftest import IMAGE_URL


@pytest.mark.parametrize(
    'verbosity, expected',
    (
        (0, ''),
        (1, 'browserstacker.screenshots - INFO - Username: user; Password: pass;\n'
            'browserstacker.screenshots - INFO - Default browser: %s;\n' % str(ScreenShotsAPI.default_browser))
    )
)
def test_init(capsys, verbosity, expected):
    ScreenShotsAPI('user', 'pass', verbosity=verbosity)
    assert capsys.readouterr()[0] == expected


@pytest.mark.parametrize(
    'call_kwargs, expected',
    (
        (
            {'method': 'GET', 'url': 'test'},
            'browserstacker.screenshots - DEBUG - Making "GET" request to "https://www.browserstack.com/test" with "{}"'
        ),
        (
            {'method': 'POST', 'url': 'test', 'json': {'a': 1}},
            'browserstacker.screenshots - DEBUG - Making "POST" request to '
            '"https://www.browserstack.com/test" with "{\'json\': {\'a\': 1}}"'
        ),
    )
)
@pytest.mark.usefixtures('mocked_request')
def test_execute_request(capsys, call_kwargs, expected):
    api = ScreenShotsAPI('user', 'pass', verbosity=2)
    api.execute(**call_kwargs)
    last_line = capsys.readouterr()[0].split('\n')[2]
    assert last_line == expected


def test_execute_response(capsys, mocked_request):
    content = '{"json": "content"}'
    mocked_request().content = content
    api = ScreenShotsAPI('user', 'pass', verbosity=2)
    api.execute('GET', 'test')
    assert capsys.readouterr()[0].split('\n')[-2] == 'browserstacker.screenshots - DEBUG - Response: "%s"' % content


def test_download(capsys, mocked_open, mocked_get, mocked_image_response, test_dir_name):
    api = ScreenShotsAPI('user', 'pass', verbosity=2)
    mocked_get.return_value = mocked_image_response
    with patch.object(api, 'list') as list_screenshots:
        list_screenshots.return_value = {'screenshots': [{'image_url': IMAGE_URL}]}
        api.download('123', test_dir_name)
    assert capsys.readouterr()[0].split('\n')[-2] == 'browserstacker.screenshots - DEBUG - Saving ' \
                                                     '"http://www.example/screenshots/test_save.jpg" to ' \
                                                     '"test_dir/test_save.jpg" ...'

# coding: utf-8
import os

import pytest

try:
    from browserstacker.cli import cli
except (SyntaxError, ImportError):
    pytest.skip()
from browserstacker.cli.helpers import format_browsers
from .conftest import LIST_BROWSERS_RESPONSE, IMAGE_URL
from ._compat import patch


@pytest.mark.usefixtures('list_browsers_response')
def test_list_browsers(isolated_cli_runner):
    result = isolated_cli_runner.invoke(cli, ['list_browsers'], catch_exceptions=False)
    assert not result.exception
    assert result.output == 'Available browsers:\n%s\nTotal browsers: %s\n' % (
        format_browsers(LIST_BROWSERS_RESPONSE), len(LIST_BROWSERS_RESPONSE)
    )


def test_list_screenshots(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {'screenshots': [{'image_url': IMAGE_URL}]}
    result = isolated_cli_runner.invoke(cli, ['-vv', 'list_screenshots', 'xxx'], catch_exceptions=False)
    assert not result.exception
    assert '{\'screenshots\': [{\'image_url\': \'%s\'}]}\n' % IMAGE_URL in result.output


def test_list_screenshots_verbose(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {'screenshots': [{'image_url': IMAGE_URL}]}
    result = isolated_cli_runner.invoke(cli, ['-vv', 'list_screenshots', 'xxx'], catch_exceptions=False)
    assert not result.exception
    assert 'browserstacker.screenshots - DEBUG - Making "GET" request ' \
           'to "https://www.browserstack.com/screenshots/xxx.json" with "{}"' in result.output


def test_list_screenshots_without_param(isolated_cli_runner):
    result = isolated_cli_runner.invoke(cli, ['list_screenshots'], catch_exceptions=False)
    assert result.exception
    assert 'Error: Missing argument "job_id".' in result.output


def test_make_screenshots(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {"job_id": "13b93a14db22872fcb5fd1c86b730a51197db319", "screenshots": []}
    result = isolated_cli_runner.invoke(cli, ['make_screenshots', 'http://www.google.com'], catch_exceptions=False)
    assert not result.exception


@pytest.mark.parametrize(
    'args, expected_path',
    (
        (['save_screenshot', IMAGE_URL], 'test_save.jpg'),
        (['save_screenshot', IMAGE_URL, '-d', 'test'], 'test/test_save.jpg'),
    )
)
def test_save_screenshot(isolated_cli_runner, mocked_get, mocked_image_response, args, expected_path):
    mocked_get.return_value = mocked_image_response
    result = isolated_cli_runner.invoke(cli, args, catch_exceptions=False)
    assert not result.exception
    assert os.path.exists(expected_path)


@pytest.mark.parametrize('is_readable', (True, False))
@pytest.mark.usefixtures('list_browsers_response')
def test_readable_io_wrapper(isolated_cli_runner, is_readable):
    """
    On real installations stdout sometimes is not readable.
    """
    with patch('click.get_text_stream') as stdout:
        stdout().readable.return_value = is_readable
        result = isolated_cli_runner.invoke(cli, ['list_browsers'], catch_exceptions=False)
        assert not result.exception
        assert stdout().read.called is is_readable

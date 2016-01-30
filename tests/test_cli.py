# coding: utf-8
import pytest

try:
    from browserstacker.cli import cli
except (SyntaxError, ImportError):
    pytest.skip()
from browserstacker.cli.helpers import format_browsers
from .conftest import LIST_BROWSERS_RESPONSE


@pytest.mark.usefixtures('list_browsers_response')
def test_list_browsers(isolated_cli_runner):
    result = isolated_cli_runner.invoke(cli, ['list_browsers'], catch_exceptions=False)
    assert not result.exception
    assert result.output == 'Available browsers:\n%s\nTotal browsers: %s\n' % (
        format_browsers(LIST_BROWSERS_RESPONSE), len(LIST_BROWSERS_RESPONSE)
    )


def test_list_screenshots(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {"screenshots": [{"image_url": "http://www.example.com/image.jpg"}]}
    result = isolated_cli_runner.invoke(cli, ['-vv', 'list_screenshots', 'xxx'], catch_exceptions=False)
    assert not result.exception
    assert '{\'screenshots\': [{\'image_url\': \'http://www.example.com/image.jpg\'}]}\n' in result.output


def test_list_screenshots_verbose(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {"screenshots": [{"image_url": "http://www.example.com/image.jpg"}]}
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

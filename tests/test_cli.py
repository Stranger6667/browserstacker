# coding: utf-8
import os

import pytest

try:
    from browserstacker.cli import cli
except (SyntaxError, ImportError):
    pytest.skip()
from browserstacker.cli.helpers import format_browsers
from .conftest import BROWSERS_RESPONSE, IMAGE_URL
from ._compat import patch


JOB_ID = '13b93a14db22872fcb5fd1c86b730a51197db319'
BROWSER = {'os': 'OS X', 'browser': 'firefox', 'os_version': 'Lion', 'browser_version': '18.0', 'device': None}


@pytest.mark.parametrize(
    'args, expected', (
        (
            ['browsers'],
            'Available browsers:\n%s\nTotal browsers: %s\n' % (
                    format_browsers(BROWSERS_RESPONSE), len(BROWSERS_RESPONSE)
            )
        ),
        (
            [
                'browsers',
                '-b', BROWSER['browser'],
                '-bv', BROWSER['browser_version'],
                '-os', BROWSER['os'],
                '-ov', BROWSER['os_version'],
            ],
            'Available browsers:\n%s\nTotal browsers: %s\n' % (format_browsers([BROWSER]), 1)
        )
    )
)
@pytest.mark.usefixtures('browsers_response')
def test_browsers(isolated_cli_runner, args, expected):
    result = isolated_cli_runner.invoke(cli, args, catch_exceptions=False)
    assert not result.exception
    assert result.output == expected


def test_list(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {'screenshots': [{'image_url': IMAGE_URL}]}
    result = isolated_cli_runner.invoke(cli, ['-vv', 'list', 'xxx'], catch_exceptions=False)
    assert not result.exception
    assert '{\'screenshots\': [{\'image_url\': \'%s\'}]}\n' % IMAGE_URL in result.output


def test_list_verbose(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {'screenshots': [{'image_url': IMAGE_URL}]}
    result = isolated_cli_runner.invoke(cli, ['-vv', 'list', 'xxx'], catch_exceptions=False)
    assert not result.exception
    assert 'browserstacker.screenshots - DEBUG - Making "GET" request ' \
           'to "https://www.browserstack.com/screenshots/xxx.json" with "{}"' in result.output


def test_list_without_param(isolated_cli_runner):
    result = isolated_cli_runner.invoke(cli, ['list'], catch_exceptions=False)
    assert result.exception
    assert 'Error: Missing argument "job_id".' in result.output


# TODO. Write real tests for screenshot generation
def test_make(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {'job_id': JOB_ID, 'screenshots': []}
    result = isolated_cli_runner.invoke(cli, ['make', 'http://www.google.com'], catch_exceptions=False)
    assert not result.exception


def test_generate(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {'job_id': JOB_ID, 'screenshots': []}
    result = isolated_cli_runner.invoke(cli, ['generate', 'http://www.google.com'], catch_exceptions=False)
    assert not result.exception


def test_generate_with_browsers(isolated_cli_runner, mocked_request):
    mocked_request().json.return_value = {'job_id': JOB_ID, 'screenshots': []}
    result = isolated_cli_runner.invoke(
        cli, ['generate', 'http://www.google.com', '-os', 'Windows'], catch_exceptions=False
    )
    assert not result.exception


def test_download(isolated_cli_runner, mocked_request, mocked_get, mocked_image_response):
    mocked_request().json.return_value = {'job_id': JOB_ID, 'screenshots': [{'image_url': IMAGE_URL, 'state': 'done'}]}
    mocked_get.return_value = mocked_image_response
    result = isolated_cli_runner.invoke(cli, ['-vv', 'download', JOB_ID], catch_exceptions=False)
    assert not result.exception
    assert 'browserstacker.screenshots - DEBUG - ' \
           'Saving "http://www.example/screenshots/test_save.jpg" to "test_save.jpg" ...' in result.output
    assert os.path.exists('test_save.jpg')


@pytest.mark.parametrize('is_readable', (True, False))
@pytest.mark.usefixtures('browsers_response')
def test_readable_io_wrapper(isolated_cli_runner, is_readable):
    """
    On real installations stdout sometimes is not readable.
    """
    with patch('click.get_text_stream') as stdout:
        stdout().readable.return_value = is_readable
        result = isolated_cli_runner.invoke(cli, ['browsers'], catch_exceptions=False)
        assert not result.exception
        assert stdout().read.called is is_readable

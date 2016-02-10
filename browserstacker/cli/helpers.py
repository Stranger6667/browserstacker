# coding: utf-8
import click

from ..screenshots import ScreenShotsAPI


DELIMITER = '\n------\n'


def format_browsers(browsers):
    return DELIMITER + DELIMITER.join(
        '\n'.join(
            '%s: %s' % item for item in browser.items()
        ) for browser in browsers
    ) + DELIMITER


def echo_stdout():
    stdout = click.get_text_stream('stdout')
    if stdout.readable():
        stdout.read()


class APIWrapper(ScreenShotsAPI):
    """
    Convenience wrapper for ScreenShotsAPI for better integration with command line.
    """

    def __getattribute__(self, item):
        result = super(APIWrapper, self).__getattribute__(item)
        echo_stdout()
        return result

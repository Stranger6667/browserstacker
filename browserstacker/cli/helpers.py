# coding: utf-8
import click

from ..screenshots import ScreenShotsAPI


def format_browsers(browsers):
    return '\n------\n'.join(
        '\n'.join(
            '%s: %s' % item for item in browser.items()
        ) for browser in browsers
    )


class APIWrapper(ScreenShotsAPI):
    """
    Convenience wrapper for ScreenShotsAPI for better integration with command line.
    """

    def __getattribute__(self, item):
        result = super(APIWrapper, self).__getattribute__(item)
        click.get_text_stream('stdout').read()
        return result

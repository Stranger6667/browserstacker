# coding: utf-8


def format_browsers(browsers):
    return '\n------\n'.join(
        '\n'.join(
            '%s: %s' % item for item in browser.items()
        ) for browser in browsers
    )

# coding: utf-8
import logging
import os
import sys

import requests
from requests.auth import HTTPBasicAuth

from ._compat import urljoin


DEFAULT_LOGGING_LEVEL = logging.CRITICAL


def get_logger(verbosity):
    """
    Returns simple console logger.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel({
        0: DEFAULT_LOGGING_LEVEL,
        1: logging.INFO,
        2: logging.DEBUG
    }.get(min(2, verbosity), DEFAULT_LOGGING_LEVEL))
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger


def match_item(key, value, item):
    """
    Check if some item matches criteria.
    """
    if isinstance(value, (list, tuple)):
        return any(match_item(key, sub_value, item) for sub_value in value)
    else:
        return key not in item or str(item.get(key)).lower() == str(value).lower()


class ScreenShotsAPI(object):
    """
    Wrapper for BrowserStack Screenshots API.
    """
    root_url = 'https://www.browserstack.com/'
    default_browser = {
        'browser_version': '37.0',
        'os': 'Windows',
        'browser': 'firefox',
        'os_version': '8.1',
        'device': None
    }

    def __init__(self, user, key, default_browser=None, verbosity=0):
        self.auth = HTTPBasicAuth(user, key)
        self.default_browser = default_browser or self.default_browser
        self.logger = get_logger(verbosity)
        self.logger.info('Username: %s; Password: %s;', user, key)
        self.logger.info('Default browser: %s;', self.default_browser)

    @property
    def session(self):
        if not hasattr(self, '_session'):
            self._session = requests.Session()
        return self._session

    def execute(self, method, url, **kwargs):
        url = urljoin(self.root_url, url)
        self.logger.debug('Making "%s" request to "%s" with "%s"', method, url, str(kwargs))
        kwargs.setdefault('auth', self.auth)
        response = self.session.request(method, url, **kwargs)
        self.logger.debug('Response: "%s"', response.content)
        return response.json()

    def browsers(self, browser=None, browser_version=None, device=None, os=None, os_version=None):
        """
        Returns list of available browsers & OS.
        """
        response = self.execute('GET', '/screenshots/browsers.json')
        for key, value in list(locals().items()):
            if key in ('self', 'response') or not value:
                continue
            response = [item for item in response if match_item(key, value, item)]
        return response

    def make(self, url, browsers=None, destination=None, **kwargs):
        """
        Generates screenshots for given settings and saves it to specified destination.
        """
        response = self.generate(url, browsers, **kwargs)
        self.download(response['job_id'], destination)

    def generate(self, url, browsers=None, orientation=None, mac_res=None, win_res=None,
                             quality=None, local=None, wait_time=None, callback_url=None):
        """
        Generates screenshots for a URL.
        """
        if isinstance(browsers, dict):
            browsers = [browsers]
        if browsers is None:
            browsers = [self.default_browser]
        data = dict((key, value) for key, value in locals().items() if value is not None and key != 'self')
        return self.execute('POST', '/screenshots', json=data)

    def list(self, job_id):
        """
        Generate the list of screenshots and their states.
        """
        return self.execute('GET', '/screenshots/%s.json' % job_id)

    def download(self, job_id, destination=None):
        """
        Downloads all screenshots for given job_id to `destination` folder.
        If `destination` is None, then screenshots will be saved in current directory.
        """
        response = self.list(job_id)
        for screenshot in response['screenshots']:
            self.save(screenshot['image_url'], destination)

    def save(self, image_url, destination=None):
        image_response = self.session.get(image_url, stream=True)
        filename = image_url.split('/')[-1]
        if destination:
            self.ensure_dir(destination)
            filename = os.path.join(destination, filename)
        self.logger.debug('Saving "%s" to "%s" ...', image_url, filename)
        self.save_file(filename, image_response)

    def ensure_dir(self, destination):
        """
        Checks, that `destination` exists.
        """
        try:
            os.makedirs(destination)
        except OSError:
            pass

    def save_file(self, filename, content):
        """
        Saves file on local filesystem.
        """
        with open(filename, 'wb') as f:
            for chunk in content.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

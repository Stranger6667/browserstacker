# coding: utf-8
import logging
import os
import sys
from time import sleep

import requests

from ._compat import urljoin


DEFAULT_LOGGING_LEVEL = logging.CRITICAL
DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 6


class AuthError(RuntimeError):
    pass


class ParallelLimitReached(RuntimeError):
    pass


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
    logger.handlers = []
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
        self.auth = requests.auth.HTTPBasicAuth(user, key)
        self.default_browser = default_browser or self.default_browser
        self._cache = {}
        self.logger = get_logger(verbosity)
        self.logger.info('Username: %s; Password: %s;', user, key)
        self.logger.info('Default browser: %s;', self.default_browser)

    def execute(self, method, url, **kwargs):
        url = urljoin(self.root_url, url)
        self.logger.debug('Making "%s" request to "%s" with "%s"', method, url, str(kwargs))
        kwargs.setdefault('auth', self.auth)
        response = requests.request(method, url, **kwargs)
        self.logger.debug('Response: "%s"', response.content)
        response = response.json()
        if isinstance(response, dict):
            if response.get('message') == 'Parallel limit reached':
                raise ParallelLimitReached
            elif response.get('error') == 'Sign up or sign in':
                raise AuthError
        return response

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

    def make(self, url, browsers=None, destination=None, timeout=DEFAULT_TIMEOUT, retries=DEFAULT_RETRIES, **kwargs):
        """
        Generates screenshots for given settings and saves it to specified destination.
        """
        response = self.generate(url, browsers, **kwargs)
        return self.download(response['job_id'], destination, timeout, retries)

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

    def download(self, job_id, destination=None, timeout=DEFAULT_TIMEOUT, retries=DEFAULT_RETRIES):
        """
        Downloads all screenshots for given job_id to `destination` folder.
        If `destination` is None, then screenshots will be saved in current directory.
        """
        self._retries_num = 0
        sleep(timeout)
        self.save_many(job_id, destination, timeout, retries)
        return self._cache

    def save_many(self, job_id, destination, timeout, retries):
        response = self.list(job_id)
        for screenshot in response['screenshots']:
            state = screenshot['state']
            if state == 'timed-out':
                continue
            if self._retries_num >= retries:
                self.logger.debug('Retry limit exceeded for %s' % job_id)
                break
            if state != 'done' or not screenshot['image_url']:
                self.logger.debug('Retrying download for %s' % job_id)
                self._retries_num += 1
                sleep(timeout)
                self.save_many(job_id, destination, timeout, retries)
                break
            self.save(screenshot['image_url'], destination)

    def save(self, image_url, destination=None):
        filename = image_url.split('/')[-1]
        if image_url in self._cache:
            return
        image_response = requests.get(image_url, stream=True)
        if destination:
            self.ensure_dir(destination)
            filename = os.path.join(destination, filename)
        self.logger.debug('Saving "%s" to "%s" ...', image_url, filename)
        self.save_file(filename, image_response)
        self._cache[image_url] = filename

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

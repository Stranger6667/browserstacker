# coding: utf-8
import os

import requests
from requests.auth import HTTPBasicAuth

from ._compat import urljoin


class ScreenShotsAPI:
    """
    Wrapper for BrowserStack Screenshots API.
    """
    root_url = 'https://www.browserstack.com/'

    def __init__(self, user, key):
        self.auth = HTTPBasicAuth(user, key)

    def execute(self, method, url, **kwargs):
        kwargs.setdefault('auth', self.auth)
        url = urljoin(self.root_url, url)
        return requests.request(method, url, **kwargs).json()

    def list_browsers(self):
        """
        Returns list of available browsers & OS.
        """
        return self.execute('GET', '/screenshots/browsers.json')

    def generate_screenshots(self, url, browsers, orientation=None, mac_res=None, win_res=None,
                             quality=None, local=None, wait_time=None, callback_url=None):
        """
        Generates screenshots for a URL.
        """
        if isinstance(browsers, dict):
            browsers = [browsers]
        data = dict((key, value) for key, value in locals().items() if value is not None and key != 'self')
        return self.execute('POST', '/screenshots', json=data)

    def list_screenshots(self, job_id):
        """
        Generate the list of screenshots and their states.
        """
        return self.execute('GET', '/screenshots/%s.json' % job_id)

    def download_screenshots(self, job_id, destination=None):
        """
        Downloads all screenshots for given job_id to `destination` folder.
        If `destination` is None, then screenshots will be saved in current directory.
        """
        response = self.list_screenshots(job_id)
        if destination:
            self.ensure_dir(destination)
        for screenshot in response['screenshots']:
            self.save_screenshot(screenshot['image_url'])

    def save_screenshot(self, image_url):
        image_response = requests.get(image_url, stream=True)
        filename = image_url.split('/')[-1]
        self.save_file(filename, image_response)

    def ensure_dir(self, destination):
        """
        Checks, that `destination` exists.
        """
        if not os.path.exists(destination):
            os.makedirs(destination)

    def save_file(self, filename, content):
        """
        Saves file on local filesystem.
        """
        with open(filename, 'wb') as f:
            for chunk in content.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

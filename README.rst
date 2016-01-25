BrowserStacker
==============
Python wrapper for BrowserStack features.

|Build Status| |codecov.io|


Installation
------------

The current stable release:

::

    pip install browserstacker

or:

::

    easy_install browserstacker

or from source:

::

    $ sudo python setup.py install

Usage
-----

To start working with BrowserStack ScreenShots API simply type:

.. code:: python

    >>> from browserstacker import ScreenShotsAPI
    >>> api = ScreenShotsAPI('user', 'key')
    >>> api.list_browsers()
    [
        {
          "os": "Windows",
          "os_version": "XP",
          "browser": "chrome"
          "browser_version": "21.0"
          "device": null
        },
        {
          "os": "ios",
          "os_version": "6.0",
          "browser": "Mobile Safari"
          "browser_version": null
          "device": "iPhone 4S (6.0)"
        }
      ....
    ]

To generate screenshots:

.. code:: python

    >>> browser = api.list_browsers()[0]
    >>> response = api.generate_screenshots('http://www.google.com', browser)

You'll get the `job_id` from response. To download screenshots:

.. code:: python

    >>> api.download_screenshots(response['job_id'], 'path_to_screenshots_dir')


All screenshots will be saved in 'path_to_screenshots_dir'.

Python support
--------------

BrowserStacker supports Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, PyPy, PyPy3 and Jython.


.. |Build Status| image:: https://travis-ci.org/Stranger6667/browserstacker.svg?branch=master
   :target: https://travis-ci.org/Stranger6667/browserstacker

.. |codecov.io| image:: https://codecov.io/github/Stranger6667/browserstacker/coverage.svg?branch=master
    :target: https://codecov.io/github/Stranger6667/browserstacker?branch=master
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
          "browser": "chrome",
          "browser_version": "21.0",
          "device": null
        },
        {
          "os": "ios",
          "os_version": "6.0",
          "browser": "Mobile Safari",
          "browser_version": null,
          "device": "iPhone 4S (6.0)"
        }
      ....
    ]

To generate screenshots:

.. code:: python

    >>> browser = api.list_browsers()[0]
    >>> response = api.generate_screenshots('http://www.google.com', browser)

Here you can pass single browsers or list of them.
You'll get the `job_id` from response. To list available screenshots for `job_id`:

.. code:: python

    >>> api.list_screenshots(response['job_id'])
    {
        "id":"13b93a14db22872fcb5fd1c86b730a51197db319",
        "state":"done",
        "callback_url": "http://staging.example.com",
        "win_res": "1024x768",
        "mac_res": "1920x1080",
        "quality": "compressed",
        "wait_time": 5,
        "screenshots": [
            {
                "os":"Windows",
                "os_version":"XP",
                "browser":"ie",
                "browser_version":"7.0",
                "id":"be9989892cbba9b9edc2c95f403050aa4996ac6a",
                "state":"done",
                "url":"www.google.com",
                "thumb_url":"https://www.browserstack.com/screenshots/13b93a14db22872fcb5fd1c86b730a51197db319/thumb_winxp_ie_7.0.jpg",
                "image_url":"https://www.browserstack.com/screenshots/13b93a14db22872fcb5fd1c86b730a51197db319/winxp_ie_7.0.png",
                "created_at":"2013-03-14 16:25:45 UTC",
            }
        ]
    }

To download screenshots:

.. code:: python

    >>> api.download_screenshots(response['job_id'], 'path_to_screenshots_dir')


All screenshots will be saved in 'path_to_screenshots_dir'. If `destination` kwarg is absent, then screenshots will be
downloaded to current working directory.
Also you can use shortcut to create & download screenshots to your local machine:

.. code:: python

    >>> response = api.make_screenshots('http://www.google.com', browser, destination='path_to_screenshots_dir')

Python support
--------------

BrowserStacker supports Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, PyPy, PyPy3 and Jython.


.. |Build Status| image:: https://travis-ci.org/Stranger6667/browserstacker.svg?branch=master
   :target: https://travis-ci.org/Stranger6667/browserstacker

.. |codecov.io| image:: https://codecov.io/github/Stranger6667/browserstacker/coverage.svg?branch=master
    :target: https://codecov.io/github/Stranger6667/browserstacker?branch=master
BrowserStacker
==============
Python wrapper for `BrowserStack <https://www.browserstack.com/>`_ features.

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
    >>> api.browsers()
    [
        {
          "os": "Windows",
          "os_version": "XP",
          "browser": "chrome",
          "browser_version": "21.0",
          "device": None
        },
        {
          "os": "ios",
          "os_version": "6.0",
          "browser": "Mobile Safari",
          "browser_version": None,
          "device": "iPhone 4S (6.0)"
        }
      ....
    ]

Optionally you can filter the output of ``browsers`` by ``browser``, ``browser_version``, ``device``, ``os`` or ``os_version``.

.. code:: python

    >>> api.browsers(os='Windows', browser='chrome')
    [
        {
          "os": "Windows",
          "os_version": "8.1",
          "browser": "chrome",
          "browser_version": "22.0",
          "device": None
        },
        {
          "os": "Windows",
          "os_version": "8.1",
          "browser": "chrome",
          "browser_version": "23.0",
          "device": None
        }
      ....
    ]

Command line:

.. code:: bash

    $ browserstacker browsers -os Windows -b chrome
    Available browsers:

    ------
    browser_version: 22.0
    os: Windows
    browser: chrome
    device: None
    os_version: 8.1
    ------
    ...
    Total browsers: 100


Filtration values are case insensitive and are casted to strings during filtration.
E.g. you can use integers for filtration by ``os_version`` parameter.
Also it is possible to filter by multiple values:

.. code:: python

    >>> api.browsers(os='Windows', browser=('chrome', 'firefox'))
    [
        {
          "os": "Windows",
          "os_version": "8.1",
          "browser": "chrome",
          "browser_version": "22.0",
          "device": None
        },
        {
          "os": "Windows",
          "os_version": "8.1",
          "browser": "firefox",
          "browser_version": "16.0",
          "device": None
        }
      ....
    ]

Command line:

.. code:: bash

    $ browserstacker browsers -os Windows -b chrome -b firefox
    Available browsers:

    ------
    browser_version: 22.0
    os: Windows
    browser: chrome
    device: None
    os_version: 8.1
    ------
    ...
    Total browsers: 215

To generate screenshots:

.. code:: python

    >>> browser = api.browsers()[0]
    >>> response = api.generate('http://www.google.com', browser)

Command line:

.. code:: bash

    $ browserstacker generate http://www.google.com -os Windows -b firefox -bv 37.0 -ov XP

Here you can pass single browsers or list of them.
You'll get the ``job_id`` from response. To list available screenshots for ``job_id``:

.. code:: python

    >>> api.list(response['job_id'])
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

Command line:

.. code:: bash

    $ browserstacker list 13b93a14db22872fcb5fd1c86b730a51197db319

To download screenshots:

.. code:: python

    >>> api.download(response['job_id'], 'path_to_screenshots_dir')

Command line:

.. code:: bash

    $ browserstacker download 13b93a14db22872fcb5fd1c86b730a51197db319 -d screenshots_dir

All screenshots will be saved in 'path_to_screenshots_dir'. If ``destination`` kwarg is absent, then screenshots will be
downloaded to current working directory.
Also you can use shortcut to create & download screenshots to your local machine:

.. code:: python

    >>> response = api.make('http://www.google.com', browser, destination='path_to_screenshots_dir')

Command line:

.. code:: bash

    $ browserstacker make -os Windows -b firefox -bv 37.0 -ov XP -d screenshots_dir

Command line interface
~~~~~~~~~~~~~~~~~~~~~~

Browserstacker comes with command line interface built with `Click <http://click.pocoo.org/>`_.
After installation ``browserstacker`` entry point will be available
It exposes almost the same API as ``ScreenShotsAPI`` does. Does not support Python 3.2.

To use CLI you have to pass user & key directly:

.. code:: bash

    $ browserstacker -u user -k key browsers
    Available browsers:
    ...
    Total browsers: 629

Or via environment variables:

.. code:: bash

    $ export BROWSERSTACK_USER=user
    $ export BROWSERSTACK_KEY=key
    $ browserstacker browsers

Help is also available:

.. code:: bash

    $ browserstacker --help
    Usage: browserstacker [OPTIONS] COMMAND [ARGS]...

    Options:
      -u, --user TEXT  Username on BrowserStack
      -k, --key TEXT   Access key
      -v, --verbosity  Verbosity level
      --version        Show the version and exit.
      --help           Show this message and exit.

    Commands:
      download
      generate
      browsers
      list
      make

Python support
--------------

BrowserStacker supports Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, PyPy, PyPy3 and Jython.
**NOTE**. CLI does not support Python 3.2.


.. |Build Status| image:: https://travis-ci.org/Stranger6667/browserstacker.svg?branch=master
   :target: https://travis-ci.org/Stranger6667/browserstacker

.. |codecov.io| image:: https://codecov.io/github/Stranger6667/browserstacker/coverage.svg?branch=master
    :target: https://codecov.io/github/Stranger6667/browserstacker?branch=master
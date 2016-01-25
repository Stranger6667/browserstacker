# coding: utf-8


try:
    from mock import patch, Mock, mock_open
except ImportError:
    from unittest.mock import patch, Mock, mock_open


try:
    import builtins
except ImportError:
    import __builtin__ as builtins

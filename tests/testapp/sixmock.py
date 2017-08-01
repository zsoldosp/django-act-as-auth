try:
    from unittest.mock import call, patch, Mock, PropertyMock, MagicMock  # noqa: E501
except:
    from mock import call, patch, Mock, PropertyMock, MagicMock  # noqa: F401

import pytest
from unittest.mock import Mock


@pytest.fixture()
def dynamo():
    mock = Mock()
    mock.readItem.return_value = {}
    mock.queryItems.return_value = []
    return mock


@pytest.fixture()
def channel():
    def _channel(channelName):
        mock = Mock()
        mock.channelName = channelName
        return mock

    return _channel

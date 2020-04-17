import pytest
from mikubot.chat_handlers.autoreplies import AutoReplies

# Common to all tests
triggerWord = 'triggerWord'
responseWord = 'responseWord'
channelName = 'user'

# =================
# Trigger
# =================


def test_handle_message_trigger_present(dynamo, channel):
    mock_channel = channel(channelName)
    dynamo.readItem.return_value = {'response': responseWord}
    ar = AutoReplies(dynamo)
    ar.handleMessage('!{}'.format(triggerWord), 'user', {}, mock_channel)

    mock_channel.writeMessage.assert_called_once_with(responseWord)


def test_handle_message_trigger_not_present(dynamo, channel):
    mock_channel = channel(channelName)
    dynamo.readItem.return_value = {}
    ar = AutoReplies(dynamo)
    ar.handleMessage('!{}'.format(triggerWord), 'user', {}, mock_channel)

    mock_channel.writeMessage.assert_not_called()

# =================
# list
# =================


def test_handle_message_list(dynamo, channel):
    mock_channel = channel(channelName)
    dynamo.queryItems.return_value = [
        {
            'trigger': 'one'
        },
        {
            'trigger': 'two'
        }
    ]
    ar = AutoReplies(dynamo)
    ar.handleMessage('!list', 'user', {}, mock_channel)

    mock_channel.writeMessage.assert_called_once_with(
        'Auto-replies are: one, two')

# =================
# remove
# =================


remove_key = {
    'channel': channelName,
    'trigger': triggerWord
}


def test_handle_message_remove_user_is_streamer(dynamo, channel):
    mock_channel = channel(channelName)
    ar = AutoReplies(dynamo)
    ar.handleMessage('!remove triggerWord', 'user', {'mod': '0'}, mock_channel)

    dynamo.removeItem.assert_called_once_with('autoreplies', remove_key)


def test_handle_message_remove_user_is_mod(dynamo, channel):
    mock_channel = channel(channelName)
    ar = AutoReplies(dynamo)
    ar.handleMessage('!remove {}'.format(triggerWord),
                     'mod', {'mod': '1'}, mock_channel)

    dynamo.removeItem.assert_called_once_with('autoreplies', remove_key)


def test_handle_message_remove_user_is_not_mod_or_streamer(dynamo, channel):
    mock_channel = channel(channelName)
    ar = AutoReplies(dynamo)
    ar.handleMessage('!remove {}'.format(triggerWord),
                     'another_user', {'mod': '0'}, mock_channel)

    dynamo.removeItem.assert_not_called()
    mock_channel.writeMessage.assert_called_once()

# =================
# set
# =================


set_key = {
    'channel': channelName,
    'trigger': triggerWord,
    'response': responseWord
}


def test_handle_message_set_user_is_streamer(dynamo, channel):
    mock_channel = channel(channelName)
    ar = AutoReplies(dynamo)
    ar.handleMessage('!set {} {}'.format(triggerWord, responseWord),
                     'user', {'mod': '0'}, mock_channel)

    dynamo.putItem.assert_called_once_with('autoreplies', set_key)


def test_handle_message_set_user_is_mod(dynamo, channel):
    mock_channel = channel(channelName)
    ar = AutoReplies(dynamo)
    ar.handleMessage('!set {} {}'.format(triggerWord, responseWord),
                     'mod', {'mod': '1'}, mock_channel)

    dynamo.putItem.assert_called_once_with('autoreplies', set_key)


def test_handle_message_set_user_is_not_mod_or_streamer(dynamo, channel):
    mock_channel = channel(channelName)
    ar = AutoReplies(dynamo)
    ar.handleMessage('!set {} {}'.format(triggerWord, responseWord),
                     'another_user', {'mod': '0'}, mock_channel)

    dynamo.putItem.assert_not_called()
    mock_channel.writeMessage.assert_called_once()

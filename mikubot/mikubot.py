import os
import socket
import boto3
import sys
from channel import Channel
from dynamo import Dynamo
from collections import namedtuple
from chat_handlers.autoreplies import AutoReplies

command_marker = '!'
dynamo = ''
isDebug = 'debug' in sys.argv
if isDebug:
    dynamo = Dynamo(boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000"))
else:
    dynamo = Dynamo(boto3.resource('dynamodb', region_name='us-west-2'))


class MikuBot:
    """
    The meat of the miku bot. This needs to be broken up into many testable chunks.

    For now it will manually join one of the two servers and receive all messages
    and hold all channel objects
    """

    handlers = [AutoReplies(dynamo)]
    channels = {}

    def start(self):
        password = os.environ.get('mikubotPass')
        nick = os.environ.get('mikubotNick')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("irc.chat.twitch.tv", 6667))

        self._sendCommand(s, "PASS {0}".format(password))
        self._sendCommand(s, "NICK {0}".format(nick))
        self._sendCommand(s, "CAP REQ :twitch.tv/tags")
        self._sendCommand(s, "JOIN #{0}".format('burnt898'))
        self._sendCommand(s, "JOIN #{0}".format('kylesgamingemporium'))

        while (1):
            buffer = s.recv(1024).decode()
            if buffer.startswith('PING :tmi.twitch.tv'):
                print('sending pong')
                self._sendCommand(s, 'PONG :tmi.twitch.tv')

            if isDebug:
                print(buffer)

            pieces = buffer.split()

            if len(pieces) >= 3:
                if pieces[1] == 'JOIN':
                    channelName = pieces[2][1:]
                    print('joining {}'.format(channelName))
                    self.channels[channelName] = Channel(channelName, s)

                if pieces[2] == 'PRIVMSG':
                    priv_msg = self._getPrivMsgInfo(buffer)
                    try:
                        channel = self.channels[priv_msg.channelName]
                    except KeyError as e:
                        print('can not send a message to {} as we are not joined'.format(
                            priv_msg.channelName))
                    else:
                        for handler in self.handlers:
                            handler.handleMessage(
                                priv_msg.message, priv_msg.user, priv_msg.tags, channel)

    def _sendCommand(self, socket, command):
        socket.sendall("{0}\n".format(command).encode())

    def _getPrivMsgInfo(self, full_message):
        """
        Parse a server IRC message that is of type PRIVMSG

        https://dev.twitch.tv/docs/irc/guide#command--message-limits
        """
        PrivMsg = namedtuple('PrivMsg', 'user message tags channelName')
        pieces = full_message.split()
        channel = pieces[3][1:]

        first_colon_index = full_message.find(':')
        first_bang_index = full_message.find('!')

        user = full_message[first_colon_index:first_bang_index]

        last_colon_index = full_message.rfind(':')
        message = full_message[last_colon_index + 1:]

        tags = {}
        for tag_pair in pieces[0][1:].split(';'):
            kv = tag_pair.split('=')
            if len(kv) == 2:
                tags[kv[0]] = kv[1]

        print(tags)

        return PrivMsg(user, message, tags, channel)


if __name__ == '__main__':
    MikuBot().start()

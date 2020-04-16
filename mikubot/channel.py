class Channel:
    """Abstract all opertations that can be performed on a twitch channel.

    This will be extended to include things like joining, leaving, listing users,
    adding ban words for example

    """

    _socket = ""  # absolutely no way this is the proper way to do this
    channelName = ""

    def __init__(self, channelName, socket):
        self.channelName = channelName
        self._socket = socket

    def writeMessage(self, message):
        """Write the given message to the underlying twitch channel"""
        self._socket.sendall('PRIVMSG #{0} :{1}\n'.format(
            self.channelName, message).encode())

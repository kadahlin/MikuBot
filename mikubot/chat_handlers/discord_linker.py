import os

burntLink = os.environ.get('burntInvite')


def handler(message, user, channel):
    if message.startswith('!discord'):
        print('sending discord link to channel [{}]'.format(
            channel.channelName))
        channel.writeMessage(burntLink)

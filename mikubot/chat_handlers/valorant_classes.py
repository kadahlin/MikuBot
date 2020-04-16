def handler(message, user, channel):
    if message.startswith('!agents'):
        print('sending valorant info to channel [{}]'.format(
            channel.channelName))
        channel.writeMessage('Viper main, with some Sage thrown in')

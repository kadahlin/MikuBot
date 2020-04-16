from boto3.dynamodb.conditions import Key, Attr
tableName = 'autoreplies'


class AutoReplies:

    _dynamo = ''

    def __init__(self, dynamo):
        self._dynamo = dynamo
        dynamo.createTable(tableName='autoreplies', partitionKey='channel', sortKey='trigger', attributeDefinitions=[
            {
                'AttributeName': 'channel',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'trigger',
                'AttributeType': 'S'
            }
        ])

    def handleMessage(self, message, user, tags, channel):
        print('auto reply for', message)
        pieces = message.split()
        if len(pieces) == 1:
            possible_trigger = pieces[0][1:]  # truncate !

            if possible_trigger == 'list':
                autoreplies = self._dynamo.queryItems(
                    tableName, Key('channel').eq(channel.channelName))
                triggers = map(lambda item: item['trigger'], autoreplies)

                channel.writeMessage(
                    'Auto-replies are: {}'.format(', '.join(triggers)))
            else:
                item = self._dynamo.readItem(tableName, {
                    'channel': channel.channelName,
                    'trigger': possible_trigger
                })

                if item:
                    channel.writeMessage(item['response'])

        if len(pieces) >= 3:
            self._possiblyHandleSet(pieces, user, tags, channel)

        if len(pieces) == 2:
            self._possiblyHandleRemove(pieces, user, tags, channel)

    def _possiblyHandleSet(self, pieces, user, tags, channel):
        if pieces[0][1:] == 'set':
            if user != channel.channelName and tags['mod'] == '0':
                channel.writeMessage(
                    'only the streamer or their mods can set replies')
                return

            trigger = pieces[1]
            response = ' '.join(pieces[2:])

            self._dynamo.putItem(tableName, {
                'channel': channel.channelName,
                'trigger': trigger,
                'response': response
            })

            print('put {} triggered by {} in {}'.format(
                response, trigger, channel.channelName))

    def _possiblyHandleRemove(self, pieces, user, tags, channel):
        if pieces[0][1:] == 'remove':
            if user != channel.channelName and tags['mod'] == '0':
                channel.writeMessage(
                    'only the streamer or their mods can remove replies')
                return

            trigger = pieces[1]

            self._dynamo.removeItem(tableName, {
                'channel': channel.channelName,
                'trigger': trigger
            })

            print('removed trigger {} for {}'.format(
                trigger, channel.channelName))

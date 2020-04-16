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

    def handleMessage(self, message, user, channel):
        print('auto reply for', message)
        pieces = message.split()
        if len(pieces) == 1:
            possible_trigger = pieces[0][1:]  # truncate !
            item = self._dynamo.readItem(tableName, {
                'channel': channel.channelName,
                'trigger': possible_trigger
            })

            if item:
                channel.writeMessage(item['response'])

        if len(pieces) == 3:
            if pieces[0][1:] == 'set':
                trigger = pieces[1]
                response = pieces[2]

                self._dynamo.putItem(tableName, {
                    'channel': channel.channelName,
                    'trigger': trigger,
                    'response': response
                })

                print('put {} triggered by {} in {}'.format(
                    response, trigger, channel.channelName))

import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


class Dynamo:
    """
    Wrap the dynamodb access for easy use across all of the features.
    """

    _dynamodb = ""

    def __init__(self, dynamodb):
        self._dynamodb = dynamodb

    def createTable(self, tableName, partitionKey, attributeDefinitions, sortKey=''):
        try:
            keySchema = [
                {'AttributeName': partitionKey, 'KeyType': 'HASH'}]
            if sortKey != '':
                keySchema.append(
                    {'AttributeName': sortKey, 'KeyType': 'RANGE'})

            table = self._dynamodb.create_table(
                TableName=tableName,
                KeySchema=keySchema,
                AttributeDefinitions=attributeDefinitions,
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            print('Table status: ', table.table_status)
        except:
            print('got error when creating table {}'.format(tableName))

    def putItem(self, tableName, attributes):
        table = self._dynamodb.Table(tableName)
        response = table.put_item(
            Item=attributes
        )

        print("PutItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))

    def readItem(self, tableName, key):
        """Return a dictionary that contains the result of this query"""
        table = self._dynamodb.Table(tableName)
        try:
            response = table.get_item(Key=key)
        except ClientError as e:
            print(e.response['Error']['Message'])
            return {}
        else:
            return response['Item']

    def removeItem(self, tableName, key):
        table = self._dynamodb.Table(tableName)
        response = table.delete_item(Key=key)
        print('deletion from {} of {} successful'.format(tableName, key))

    def deleteTable(self, tableName):
        table = self._dynamodb.Table(tableName)
        table.delete()
        print('successfully deleted table: ', tableName)


class DecimalEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


if __name__ == '__main__':
    dynamodb = boto3.resource(
        'dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    dynamo = Dynamo(dynamodb)

    dynamo.createTable('testing', 'name', [{
        'AttributeName': 'name',
        'AttributeType': 'S'
    }])

    dynamo.putItem('testing', {
        'name': 'testName'
    })

    item = dynamo.readItem('testing', {'name': 'testName'})
    print(json.dumps(item, indent=4, cls=DecimalEncoder))

    dynamo.removeItem('testing', {'name': 'testName'})
    dynamo.deleteTable('testing')


import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError


class AWSIdentityCheck:
    '''Just a Utility Script that allows people to check which AWS Identity is active'''

    def __init__(self):
        pass

    def check(self):
        '''Check the AWS Identity'''
        try:
            client = boto3.client('sts')
            identity = client.get_caller_identity()
            return {
                'UserId': identity.get('UserId'),
                'Account': identity.get('Account'),
                'Arn': identity.get('Arn')
            }
        except (NoCredentialsError, BotoCoreError, ClientError) as e:
            return {'Error': str(e)}

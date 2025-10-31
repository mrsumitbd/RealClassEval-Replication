
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError


class AWSIdentityCheck:

    def __init__(self):
        self.sts_client = boto3.client('sts')
        self.identity = None
        self.error = None

    def check(self):
        try:
            self.identity = self.sts_client.get_caller_identity()
            return {
                'UserId': self.identity.get('UserId'),
                'Account': self.identity.get('Account'),
                'Arn': self.identity.get('Arn')
            }
        except (NoCredentialsError, BotoCoreError, ClientError) as e:
            self.error = str(e)
            return {'error': self.error}

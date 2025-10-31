
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


class AWSIdentityCheck:
    '''Just a Utility Script that allows people to check which AWS Identity is active'''

    def __init__(self):
        '''AWSIdentityCheck Initialization'''
        self.sts_client = boto3.client('sts')

    def check(self):
        '''Check the AWS Identity'''
        try:
            response = self.sts_client.get_caller_identity()
            return {
                'UserId': response['UserId'],
                'Account': response['Account'],
                'Arn': response['Arn']
            }
        except NoCredentialsError:
            return {'error': 'No AWS credentials found'}
        except ClientError as e:
            return {'error': str(e)}

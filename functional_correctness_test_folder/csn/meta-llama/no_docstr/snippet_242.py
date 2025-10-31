
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class AWSIdentityCheck:

    def __init__(self):
        self.sts = boto3.client('sts')

    def check(self):
        try:
            response = self.sts.get_caller_identity()
            return {
                'success': True,
                'user_id': response['UserId'],
                'account': response['Account'],
                'arn': response['Arn']
            }
        except NoCredentialsError:
            return {
                'success': False,
                'error': 'No AWS credentials found'
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }

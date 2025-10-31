
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class AWSIdentityCheck:
    '''Just a Utility Script that allows people to check which AWS Identity is active'''

    def __init__(self):
        '''AWSIdentityCheck Initialization'''
        self.session = boto3.Session()

    def check(self):
        '''Check the AWS Identity'''
        try:
            sts_client = self.session.client('sts')
            response = sts_client.get_caller_identity()
            return response['Arn']
        except NoCredentialsError:
            return "No AWS credentials found."
        except PartialCredentialsError:
            return "Incomplete AWS credentials provided."
        except Exception as e:
            return f"An error occurred: {str(e)}"

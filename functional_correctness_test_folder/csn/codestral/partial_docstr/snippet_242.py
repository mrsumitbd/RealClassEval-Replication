
import boto3


class AWSIdentityCheck:
    '''Just a Utility Script that allows people to check which AWS Identity is active'''

    def __init__(self):
        self.sts_client = boto3.client('sts')

    def check(self):
        '''Check the AWS Identity'''
        identity = self.sts_client.get_caller_identity()
        return identity

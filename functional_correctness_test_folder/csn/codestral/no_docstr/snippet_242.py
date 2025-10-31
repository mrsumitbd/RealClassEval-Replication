
import boto3


class AWSIdentityCheck:

    def __init__(self):
        self.client = boto3.client('sts')

    def check(self):
        try:
            response = self.client.get_caller_identity()
            return response
        except Exception as e:
            return str(e)

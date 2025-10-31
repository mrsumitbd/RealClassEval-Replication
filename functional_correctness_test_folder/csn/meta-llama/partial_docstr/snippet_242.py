
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class AWSIdentityCheck:
    '''Just a Utility Script that allows people to check which AWS Identity is active'''

    def __init__(self):
        self.sts_client = boto3.client('sts')

    def check(self):
        '''Check the AWS Identity'''
        try:
            response = self.sts_client.get_caller_identity()
            print("AWS Identity Check:")
            print(f"  - Account: {response['Account']}")
            print(f"  - ARN: {response['Arn']}")
            print(f"  - UserId: {response['UserId']}")
        except NoCredentialsError:
            print("No AWS credentials found. Please configure your AWS credentials.")
        except ClientError as e:
            print(f"An error occurred: {e}")


# Example usage:
if __name__ == "__main__":
    identity_check = AWSIdentityCheck()
    identity_check.check()

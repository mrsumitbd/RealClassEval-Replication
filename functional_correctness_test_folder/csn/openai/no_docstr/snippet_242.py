
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class AWSIdentityCheck:
    """
    A simple helper to retrieve the AWS caller identity using STS.
    """

    def __init__(self):
        """
        Initializes an STS client. No arguments are required; the client
        will use the default credential chain.
        """
        self.sts_client = boto3.client("sts")

    def check(self):
        """
        Retrieves the caller identity from AWS STS.

        Returns:
            dict: The response from sts.get_caller_identity().

        Raises:
            BotoCoreError, ClientError: If the request fails.
        """
        try:
            response = self.sts_client.get_caller_identity()
            return response
        except (BotoCoreError, ClientError) as exc:
            raise

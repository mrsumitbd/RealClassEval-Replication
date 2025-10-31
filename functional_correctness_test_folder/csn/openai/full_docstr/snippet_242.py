
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError


class AWSIdentityCheck:
    """Utility to determine the currently active AWS identity.

    The class uses the AWS Security Token Service (STS) to retrieve the
    caller identity.  It works with any credentials that boto3 can
    discover (environment variables, shared credentials file, IAM role,
    etc.).  If no credentials are available, an informative exception
    is raised.
    """

    def __init__(self):
        """Create an STS client using boto3."""
        self._sts = boto3.client("sts")

    def check(self):
        """
        Retrieve the current AWS identity.

        Returns
        -------
        dict
            A dictionary containing the following keys:
            - Account: AWS account ID
            - UserId: The unique identifier for the user or role
            - Arn: The Amazon Resource Name of the identity

        Raises
        ------
        RuntimeError
            If AWS credentials are not configured or the STS call fails.
        """
        try:
            response = self._sts.get_caller_identity()
        except (NoCredentialsError, BotoCoreError, ClientError) as exc:
            raise RuntimeError(
                "Unable to retrieve AWS identity. "
                "Check that AWS credentials are configured."
            ) from exc

        return {
            "Account": response.get("Account"),
            "UserId": response.get("UserId"),
            "Arn": response.get("Arn"),
        }

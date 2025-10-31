
import boto3
import botocore.exceptions


class AWSIdentityCheck:
    """Utility class to determine the currently active AWS identity.

    The class uses the AWS Security Token Service (STS) to retrieve the
    caller identity.  It works with any credentials that are available
    in the environment (environment variables, shared credentials file,
    instance profile, etc.).

    Example
    -------
    >>> checker = AWSIdentityCheck()
    >>> identity = checker.check()
    >>> print(identity)
    {'Account': '123456789012', 'Arn': 'arn:aws:iam::123456789012:user/JohnDoe', 'UserId': 'AIDAEXAMPLE'}
    """

    def __init__(self):
        """
        Create an STS client using the default session.
        """
        self._sts = boto3.client("sts")

    def check(self):
        """
        Retrieve the current AWS identity.

        Returns
        -------
        dict
            A dictionary containing the keys 'Account', 'Arn', and 'UserId'.

        Raises
        ------
        RuntimeError
            If the STS call fails or the credentials are not available.
        """
        try:
            response = self._sts.get_caller_identity()
        except botocore.exceptions.BotoCoreError as exc:
            raise RuntimeError(
                f"Failed to retrieve AWS identity: {exc}") from exc

        # The response contains 'Account', 'Arn', and 'UserId'.
        return {
            "Account": response.get("Account"),
            "Arn": response.get("Arn"),
            "UserId": response.get("UserId"),
        }

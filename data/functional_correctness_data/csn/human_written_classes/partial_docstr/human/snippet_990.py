from botocore.credentials import RefreshableCredentials
import boto3
from botocore.session import get_session

class AwsSessionHelper:
    """ The AwsSessionHelper creates a auto-refreshable boto3 session object
        and allows for creating clients with those refreshable credentials.
    """

    def __init__(self, session_name, role_arn, region='us-east-1', s3_role_session_duration_s=3600):
        """ session_name: str; The name of the session we are creating
            role_arn: str; The ARN of the role we are assuming with STS
            region: str; The region for the STS client to be created in
            s3_role_session_duration_s: int; the time that session is good for
        """
        self.role_arn = role_arn
        self.session_name = session_name
        self.region = region
        self.session_duration_seconds = s3_role_session_duration_s
        self.sts_client = boto3.client('sts')
        credentials = self._refresh()
        session_credentials = RefreshableCredentials.create_from_metadata(metadata=credentials, refresh_using=self._refresh, method='sts-assume-role')
        aws_session = get_session()
        aws_session._credentials = session_credentials
        aws_session.set_config_variable('region', region)
        self.aws_session = boto3.Session(botocore_session=aws_session)

    def get_client(self, service):
        """ Returns boto3.client with the refreshable session

            service: str; String of what service to create a client for
            (e.g. 'sqs', 's3')
        """
        return self.aws_session.client(service)

    def get_session(self):
        """ Returns the raw refreshable aws session
        """
        return self.aws_session

    def _refresh(self):
        params = {'RoleArn': self.role_arn, 'RoleSessionName': self.session_name, 'DurationSeconds': self.session_duration_seconds}
        response = self.sts_client.assume_role(**params).get('Credentials')
        credentials = {'access_key': response.get('AccessKeyId'), 'secret_key': response.get('SecretAccessKey'), 'token': response.get('SessionToken'), 'expiry_time': response.get('Expiration').isoformat()}
        return credentials
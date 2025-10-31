import logging
from workbench.core.cloud_platform.aws.aws_account_clamp import AWSAccountClamp

class WorkbenchSQS:

    def __init__(self, queue_url='workbench.fifo'):
        """WorkbenchSQS: Class for retrieving messages from the AWS SQS Message Queue"""
        self.log = logging.getLogger('workbench')
        self.queue_url = queue_url
        self.boto3_session = AWSAccountClamp().boto3_session
        print(self.boto3_session)
        self.sqs = self.boto3_session.client('sqs')

    def get_message(self, delete=False):
        """Get a message from the SQS Message Queue
        Args:
            delete (bool): Delete the message from the Queue after reading it
        """
        response = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=1, MessageAttributeNames=['All'], VisibilityTimeout=0, WaitTimeSeconds=0)
        status = response['ResponseMetadata']['HTTPStatusCode']
        if status != 200:
            self.log.critical(f'SQS Get Message Failure: {response}')
            return None
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        message_body = message['Body']
        if delete:
            self.sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt_handle)
        return message_body
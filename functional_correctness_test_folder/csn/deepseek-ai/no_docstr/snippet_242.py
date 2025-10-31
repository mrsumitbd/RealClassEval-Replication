
class AWSIdentityCheck:

    def __init__(self):
        self.identity = None

    def check(self):
        import boto3
        try:
            sts_client = boto3.client('sts')
            response = sts_client.get_caller_identity()
            self.identity = response
            return True
        except Exception as e:
            return False

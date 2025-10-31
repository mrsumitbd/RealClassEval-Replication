from workbench.core.cloud_platform.aws.aws_account_clamp import AWSAccountClamp
from workbench.utils.config_manager import ConfigManager
import sys
import logging

class AWSIdentityCheck:
    """Just a Utility Script that allows people to check which AWS Identity is active"""

    def __init__(self):
        """AWSIdentityCheck Initialization"""
        self.log = logging.getLogger('workbench')
        self.aws_clamp = AWSAccountClamp()

    def check(self):
        """Check the AWS Identity"""
        cm = ConfigManager()
        active_profile = cm.get_config('AWS_PROFILE')
        if active_profile:
            self.log.info(f'Workbench AWS_PROFILE: {active_profile}')
        else:
            self.log.info('No AWS_PROFILE set')
            sys.exit(0)
        self.log.info('\n\n*** Caller/Base Identity Check ***')
        self.aws_clamp.check_aws_identity()
        self.log.info('Caller/Base Identity Check Success...')
        self.log.info('\n\n*** AWS Assumed Role Check ***')
        self.aws_clamp.check_assumed_role()
        self.log.info('Assumed Role Check Success...')
import os
import uuid
import logging

class AmazonBedrockSessionManager:
    """
    Manages the AWS agent session lifecycle.
    """

    def __init__(self, client_key, client_secret, deployment_region, agent_id, alias_id, session_id):
        """
        Initializes the AmazonBedrockSessionManager.

        Args:
            client_key: The mapping to the variable that holds the AWS client key.
            client_secret: The mapping to the variable that holds the AWS client secret.
            deployment_region: The region where the AWS agent is deployed.
            agent_id: The identifier of the created AWS agent.
            alias_id: The alias identifier  for the AWS agent.
            session_id: The identifier of the session where the messages will be posted.
        """
        self.client_key = client_key
        self.client_secret = client_secret
        self.deployment_region = deployment_region
        self.agent_id = agent_id
        self.alias_id = alias_id
        self.session_id = session_id
        self.initialize_client()

    def initialize_client(self):
        try:
            self.client = boto3.client(service_name='bedrock-agent-runtime', region_name=self.deployment_region, aws_access_key_id=os.getenv(self.client_key), aws_secret_access_key=os.getenv(self.client_secret))
            logger.info('Successfully initialized AWS client.')
        except Exception:
            logger.exception('Failed to initialize AWS client')
            raise

    def initiate_session(self):
        """Creates a new session for the AWS agent"""
        self.session_id = str(uuid.uuid4()).replace('-', '')
        logger.info('Successfully created new session %s.', self.session_id)

    def send_message(self, prompt):
        """
        Sends a message to the AWS agent.
        """
        try:
            response = self.client.invoke_agent(agentId=self.agent_id, agentAliasId=self.alias_id, enableTrace=True, sessionId=self.session_id, inputText=prompt, streamingConfigurations={'applyGuardrailInterval': 20, 'streamFinalResponse': False})
            completion = ''
            for event in response.get('completion'):
                if 'chunk' in event:
                    chunk = event['chunk']
                    completion += chunk['bytes'].decode()
                if 'trace' in event:
                    trace_event = event.get('trace')
                    trace = trace_event['trace']
                    for key, value in trace.items():
                        logging.info('%s: %s', key, value)
            return completion
        except ClientError as e:
            print(f'Client error: {str(e)}')
            logger.error('Client error: %s', {str(e)})
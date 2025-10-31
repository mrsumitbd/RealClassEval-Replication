import os
from databricks.sdk import WorkspaceClient

class DatabricksSessionManager:
    """
    Manages the Databricks agent session.
    """

    def __init__(self, client_id_env_var, client_secret_env_var, host_url_env_var, genie_space_id_env_var):
        """
        Initializes the DatabricksSessionManager.

        Args:
            genie_space_id: The Databricks Genie space ID.
        """
        self._client_id = os.getenv(client_id_env_var, '')
        self._client_secret = os.getenv(client_secret_env_var, '')
        self._host_url = os.getenv(host_url_env_var, '')
        self._genie_space_id = os.getenv(genie_space_id_env_var, '')
        self._conversation_id = None

    def get_workspace_client(self):
        """
        Initialize Databricks Workspace client
        """
        self.client = WorkspaceClient(host=self._host_url, client_id=self._client_id, client_secret=self._client_secret)

    def run_query_attachments(self, response):
        query_result = self.client.genie.get_message_attachment_query_result(self._genie_space_id, response.conversation_id, response.id, response.attachments[0].attachment_id)
        sr = query_result.statement_response
        if not sr or not sr.result or (not sr.result.data_array):
            raise ValueError('statement_response or its nested attributes are None')
        return sr.result.data_array

    def start_genie_conversation(self, workspace_client, space_id, message):
        """
        Initiate new conversation with Genie agent
        """
        response = workspace_client.genie.start_conversation_and_wait(space_id=space_id, content=message)
        return response

    def continue_genie_conversation(self, workspace_client, space_id, conversation_id, prompt):
        """
        Continue previous conversation with Genie agent
        """
        response = workspace_client.genie.create_message_and_wait(space_id, conversation_id, prompt)
        return response

    def send_message(self, prompt):
        """
        Send message to Genie agent.
        If no conversation is active, initiate new one, otherwise post to existing.
        If the initial Genie response contains a SQL query, run it and return the results.

        Returns:
            - response (GenieMessage): struct with the raw genie response
            - sql_df (list of lists): dataframe with the result of running the
                                      SQL query attached in the original response struct
        """
        if not self._conversation_id:
            response = self.start_genie_conversation(self.client, self._genie_space_id, prompt)
            self._conversation_id = response.conversation_id
        else:
            response = self.continue_genie_conversation(self.client, self._genie_space_id, self._conversation_id, prompt)
        sql_df = []
        if not response.attachments:
            raise ValueError('response has no attachments')
        if response.attachments[0].query:
            sql_df = self.run_query_attachments(response)
        return (response, sql_df)
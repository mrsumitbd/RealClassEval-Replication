class ClientOutputCollector:

    def __init__(self, client):
        self.client = client

    def collect_output(self, results_collector, output_type, action, name):
        if not action.staging_action_local:
            return False
        working_directory = results_collector.client_outputs.working_directory
        self.client.fetch_output(path=action.path, name=name, working_directory=working_directory, output_type=output_type, action_type=action.action_type)
        return True
import os

class PulsarServerOutputCollector:

    def __init__(self, job_directory, action_executor, was_cancelled):
        self.job_directory = job_directory
        self.action_executor = action_executor
        self.was_cancelled = was_cancelled

    def collect_output(self, results_collector, output_type, action, name):

        def action_if_not_cancelled():
            if self.was_cancelled():
                log.info(f"Skipped output collection '{name}', job is cancelled")
                return
            action.write_from_path(pulsar_path)
        if action.staging_action_local:
            return
        if not name:
            name = os.path.basename(action.path)
        pulsar_path = self.job_directory.calculate_path(name, output_type)
        description = 'staging out file {} via {}'.format(pulsar_path, action)
        self.action_executor.execute(action_if_not_cancelled, description)
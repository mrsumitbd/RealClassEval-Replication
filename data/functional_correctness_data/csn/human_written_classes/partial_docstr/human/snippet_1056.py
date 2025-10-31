import os

class TaskRun:

    def __init__(self, os, task_run_name):
        self.os = os
        self.task_run_name = task_run_name
        self.api_path = 'apis'
        self.api_version = API_VERSION

    def get_info(self, wait=False):
        if wait:
            self.wait_for_start()
        url = self.os.build_url(self.api_path, self.api_version, f'taskruns/{self.task_run_name}')
        response = self.os.get(url)
        return check_response_json(response, 'get_info')

    def get_logs(self, follow=False, wait=False):
        if follow or wait:
            task_run = self.wait_for_start()
        else:
            task_run = self.get_info()
        if not task_run and (not self.get_info()):
            return
        pod_name = task_run['status']['podName']
        containers = [step['container'] for step in task_run['status']['steps']]
        pod = Pod(os=self.os, pod_name=pod_name, containers=containers)
        return pod.get_logs(follow=follow, wait=wait)

    def wait_for_start(self):
        """
        https://tekton.dev/docs/pipelines/taskruns/#monitoring-execution-status
        """
        logger.info("Waiting for task run '%s' to start", self.task_run_name)
        for task_run in self.os.watch_resource(self.api_path, self.api_version, resource_type='taskruns', resource_name=self.task_run_name):
            if not task_run and (not self.get_info()):
                logger.info("Task run '%s' does not exist", self.task_run_name)
                return
            try:
                status = task_run['status']['conditions'][0]['status']
                reason = task_run['status']['conditions'][0]['reason']
            except KeyError:
                logger.debug("Task run '%s' does not have any status yet", self.task_run_name)
                continue
            if status in ['True', 'False'] or (status == 'Unknown' and reason == 'Running'):
                logger.info("Task run '%s' started", self.task_run_name)
                return task_run
            else:
                logger.debug('Waiting for task run, current status: %s, reason %s', status, reason)
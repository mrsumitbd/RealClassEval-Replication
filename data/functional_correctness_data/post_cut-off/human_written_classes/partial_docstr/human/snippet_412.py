from pathlib import Path
import time
from src.model_config import ModelConfig
from src.factory import MCPServiceFactory
from src.agents import MCPMarkAgent
from src.errors import is_retryable_error
from datetime import datetime
import shutil
from typing import List, Optional
from src.results_reporter import EvaluationReport, ResultsReporter, TaskResult
import json

class MCPEvaluator:

    def __init__(self, mcp_service: str, model: str, timeout: int=300, exp_name: str='test-run', output_dir: Path=None, reasoning_effort: str='default'):
        self.mcp_service = mcp_service
        self.timeout = timeout
        self.reasoning_effort = reasoning_effort
        self.model_name = model
        model_config = ModelConfig(self.model_name)
        self.api_key = model_config.api_key
        self.base_url = model_config.base_url
        self.litellm_input_model_name = model_config.litellm_input_model_name
        self.litellm_run_model_name = None
        self.task_manager = MCPServiceFactory.create_task_manager(mcp_service)
        self.state_manager = MCPServiceFactory.create_state_manager(mcp_service)
        self.service_config = self.state_manager.get_service_config_for_agent()
        self.agent = MCPMarkAgent(litellm_input_model_name=self.litellm_input_model_name, api_key=self.api_key, base_url=self.base_url, mcp_service=mcp_service, timeout=timeout, service_config=self.service_config, service_config_provider=self.state_manager.get_service_config_for_agent, reasoning_effort=self.reasoning_effort)
        self.results_reporter = ResultsReporter()
        if self.reasoning_effort != 'default':
            model_slug = self.model_name.replace('.', '-') + '-' + self.reasoning_effort
        else:
            model_slug = self.model_name.replace('.', '-')
        service_for_dir = 'playwright' if mcp_service == 'playwright_webarena' else mcp_service
        self.base_experiment_dir = output_dir / f'{model_slug}__{service_for_dir}' / exp_name
        self.base_experiment_dir.mkdir(parents=True, exist_ok=True)

    def _format_duration(self, seconds: float) -> str:
        """Format duration: <1s as ms, otherwise seconds."""
        return f'{seconds * 1000:.2f}ms' if seconds < 1 else f'{seconds:.2f}s'

    def _get_task_output_dir(self, task) -> Path:
        """Return the directory path for storing this task's reports using '__' separator."""
        category_id = task.category_id if task.category_id else 'uncategorized'
        task_id = str(task.task_id)
        return self.base_experiment_dir / f'{category_id}__{task_id}'

    def _load_latest_task_result(self, task) -> Optional[TaskResult]:
        """Return the most recent TaskResult for *task* if it has been run before."""
        task_dir = self._get_task_output_dir(task)
        if not task_dir.exists():
            return None
        meta_path = task_dir / 'meta.json'
        if not meta_path.exists():
            return None
        try:
            with meta_path.open('r', encoding='utf-8') as f:
                meta_data = json.load(f)
            return TaskResult(task_name=meta_data['task_name'], success=meta_data['execution_result']['success'], error_message=meta_data['execution_result'].get('error_message'), verification_error=meta_data['execution_result'].get('verification_error'), verification_output=meta_data['execution_result'].get('verification_output'), category_id=task.category_id, task_id=task.task_id, model_output=None, token_usage=meta_data.get('token_usage', {}), turn_count=meta_data.get('turn_count'), agent_execution_time=meta_data.get('agent_execution_time', 0.0), task_execution_time=meta_data.get('task_execution_time', 0.0))
        except Exception as exc:
            logger.warning('Failed to load existing result for %s: %s', task.name, exc)
        return None

    def _gather_all_task_results(self) -> List[TaskResult]:
        """Scan *all* task sub-directories and collect the latest TaskResult from each."""
        results: list[TaskResult] = []
        if not self.base_experiment_dir.exists():
            return results
        for task_dir in self.base_experiment_dir.iterdir():
            if not task_dir.is_dir():
                continue
            meta_path = task_dir / 'meta.json'
            if not meta_path.exists():
                continue
            try:
                with meta_path.open('r', encoding='utf-8') as f:
                    meta_data = json.load(f)
                category_id, task_id = task_dir.name.split('__', 1)
                result = TaskResult(task_name=meta_data['task_name'], success=meta_data['execution_result']['success'], error_message=meta_data['execution_result'].get('error_message'), verification_error=meta_data['execution_result'].get('verification_error'), verification_output=meta_data['execution_result'].get('verification_output'), category_id=category_id, task_id=task_id, model_output=None, token_usage=meta_data.get('token_usage', {}), turn_count=meta_data.get('turn_count'), agent_execution_time=meta_data.get('agent_execution_time', 0.0), task_execution_time=meta_data.get('task_execution_time', 0.0))
                results.append(result)
            except Exception as exc:
                logger.warning('Failed to parse existing report in %s: %s', task_dir, exc)
        return results

    def _run_single_task(self, task) -> TaskResult:
        """
        Runs a single task, including setup, agent execution, verification, and cleanup.
        """
        task_start_time = time.time()
        setup_start_time = time.time()
        logger.info('\n┌─ Stage 1: Setup ─────────────────────────────────────────────────────')
        setup_success = self.state_manager.set_up(task)
        setup_time = time.time() - setup_start_time
        if not setup_success:
            logger.error(f'| State setup failed for task: {task.name}')
            task_total_time = time.time() - task_start_time
            return TaskResult(task_name=task.name, success=False, error_message='State Duplication Error', verification_error=None, verification_output=None, category_id=task.category_id, task_id=task.task_id, agent_execution_time=0.0, task_execution_time=task_total_time)
        display_time = self._format_duration(setup_time)
        logger.info(f'└─ Completed in {display_time}\n')
        logger.info('┌─ Stage 2: Execute ───────────────────────────────────────────────────')
        agent_execution_start_time = time.time()
        task_instruction = self.task_manager.get_task_instruction(task)
        task_output_dir = self._get_task_output_dir(task)
        task_output_dir.mkdir(parents=True, exist_ok=True)
        execution_log_path = task_output_dir / 'execution.log'
        if execution_log_path.exists():
            execution_log_path.unlink()
        agent_result = self.agent.execute_sync(task_instruction, str(execution_log_path))
        agent_execution_time = time.time() - agent_execution_start_time
        if agent_result.get('litellm_run_model_name'):
            self.litellm_run_model_name = agent_result['litellm_run_model_name']
        messages_path = task_output_dir / 'messages.json'
        self.results_reporter.save_messages_json(agent_result.get('output', []), messages_path)
        self.state_manager.set_verification_environment(str(messages_path))
        logger.info(f'└─ Completed in {self._format_duration(agent_execution_time)}\n')
        logger.info('┌─ Stage 3: Verify ────────────────────────────────────────────────────')
        verify_start_time = time.time()
        try:
            result = self.task_manager.execute_task(task, agent_result)
        finally:
            import os
            os.environ.pop('MCP_MESSAGES', None)
            os.environ.pop('MCP_GITHUB_TOKEN', None)
        verify_time = time.time() - verify_start_time
        logger.info(f'└─ Completed in {self._format_duration(verify_time)}\n')
        logger.info('┌─ Stage 4: Cleanup ───────────────────────────────────────────────────')
        cleanup_start_time = time.time()
        self.state_manager.clean_up(task)
        cleanup_time = time.time() - cleanup_start_time
        logger.info(f'└─ Completed in {self._format_duration(cleanup_time)}\n')
        task_total_time = time.time() - task_start_time
        result.agent_execution_time = agent_execution_time
        result.task_execution_time = task_total_time
        return result

    def run_evaluation(self, task_filter: str) -> EvaluationReport:
        """
        Runs the full evaluation for the specified tasks.
        """
        tasks = self.task_manager.filter_tasks(task_filter)
        results = []
        for task in tasks:
            existing_result = self._load_latest_task_result(task)
            retry_due_to_error = existing_result is not None and (not existing_result.success) and is_retryable_error(existing_result.error_message)
            if existing_result and (not retry_due_to_error):
                logger.info('↩️  Skipping already-completed task (resume): %s', task.name)
                results.append(existing_result)
                continue
            if retry_due_to_error:
                task_output_dir = self._get_task_output_dir(task)
                if task_output_dir.exists():
                    shutil.rmtree(task_output_dir)
                logger.info('🔄 Retrying task due to pipeline error (%s): %s', existing_result.error_message, task.name)
            task_start = time.time()
            task_result = self._run_single_task(task)
            task_end = time.time()
            results.append(task_result)
            task_output_dir = self._get_task_output_dir(task)
            task_output_dir.mkdir(parents=True, exist_ok=True)
            messages_path = task_output_dir / 'messages.json'
            if not messages_path.exists():
                messages = task_result.model_output if getattr(task_result, 'model_output', None) else []
                self.results_reporter.save_messages_json(messages, messages_path)
            meta_path = task_output_dir / 'meta.json'
            model_config = {'mcp_service': self.mcp_service, 'model_name': self.model_name, 'litellm_run_model_name': self.litellm_run_model_name, 'reasoning_effort': self.reasoning_effort, 'timeout': self.timeout}
            self.results_reporter.save_meta_json(task_result, model_config, datetime.fromtimestamp(task_start), datetime.fromtimestamp(task_end), meta_path)

        def _matches_filter(tr: TaskResult, flt: str) -> bool:
            if flt.lower() == 'all':
                return True
            if '/' in flt:
                category_id, task_id = flt.split('/', 1)
                return tr.category_id == category_id and str(tr.task_id) == task_id
            return tr.category_id == flt
        existing_results = [r for r in self._gather_all_task_results() if _matches_filter(r, task_filter)]
        merged: dict[str, TaskResult] = {r.task_name: r for r in existing_results}
        merged.update({r.task_name: r for r in results})
        final_results = list(merged.values())
        aggregated_report = EvaluationReport(model_name=self.model_name, model_config={'mcp_service': self.mcp_service, 'model_name': self.model_name, 'litellm_run_model_name': self.litellm_run_model_name, 'reasoning_effort': self.reasoning_effort, 'timeout': self.timeout}, total_tasks=len(final_results), successful_tasks=sum((1 for r in final_results if r.success)), failed_tasks=sum((1 for r in final_results if not r.success)), task_results=final_results, tasks_filter=task_filter)
        summary_path = self.base_experiment_dir / 'summary.json'
        self.results_reporter.save_model_summary(aggregated_report, summary_path)
        logger.info('\n============================================================\nResults Summary\n============================================================')
        logger.info(f'✓ Tasks passed: {aggregated_report.successful_tasks}/{aggregated_report.total_tasks} ({aggregated_report.success_rate:.1f}%)')
        logger.info(f'⏱ Total time: {aggregated_report.total_task_execution_time:.1f}s')
        return aggregated_report
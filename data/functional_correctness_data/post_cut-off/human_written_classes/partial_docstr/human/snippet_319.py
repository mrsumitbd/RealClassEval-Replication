from rich.layout import Layout
from tau2.data_model.tasks import Action, Task
import json
from rich.panel import Panel
from tau2.data_model.message import AssistantMessage, Message, SystemMessage, ToolMessage, UserMessage
from rich.text import Text
from rich.table import Table
from rich.console import Console
from tau2.data_model.simulation import RunConfig, SimulationRun
from tau2.metrics.agent_metrics import AgentMetrics, is_successful

class ConsoleDisplay:
    console = Console()

    @classmethod
    def display_run_config(cls, config: RunConfig):
        layout = Layout()
        layout.split(Layout(name='header'), Layout(name='body'))
        layout['body'].split_row(Layout(name='agent', ratio=1), Layout(name='user', ratio=1), Layout(name='settings', ratio=1))
        header_content = Panel(f"[white]Domain:[/] {config.domain}\n[white]Task Set:[/] {(config.task_set_name if config.task_set_name else 'Default')}\n[white]Task IDs:[/] {(', '.join(map(str, config.task_ids)) if config.task_ids else 'All')}\n[white]Number of trials:[/] {config.num_trials}\n[white]Max steps:[/] {config.max_steps}\n[white]Max errors:[/] {config.max_errors}", title='[bold blue]Simulation Configuration', border_style='blue')
        agent_content = Panel(f'[white]Implementation:[/] {config.agent}\n[white]Model:[/] {config.llm_agent}\n[white]LLM Arguments:[/]\n{json.dumps(config.llm_args_agent, indent=2)}', title='[bold cyan]Agent Configuration', border_style='cyan')
        user_content = Panel(f'[white]Implementation:[/] {config.user}\n[white]Model:[/] {config.llm_user}\n[white]LLM Arguments:[/]\n{json.dumps(config.llm_args_user, indent=2)}', title='[bold cyan]User Configuration', border_style='cyan')
        settings_content = Panel(f"[white]Save To:[/] {config.save_to or 'Not specified'}\n[white]Max Concurrency:[/] {config.max_concurrency}", title='[bold cyan]Additional Settings', border_style='cyan')
        layout['header'].update(header_content)
        layout['agent'].update(agent_content)
        layout['user'].update(user_content)
        layout['body']['settings'].update(settings_content)
        cls.console.print(layout)

    @classmethod
    def display_task(cls, task: Task):
        content_parts = []
        if task.id is not None:
            content_parts.append(f'[white]ID:[/] {task.id}')
        if task.description:
            if task.description.purpose:
                content_parts.append(f'[white]Purpose:[/] {task.description.purpose}')
            if task.description.relevant_policies:
                content_parts.append(f'[white]Relevant Policies:[/] {task.description.relevant_policies}')
            if task.description.notes:
                content_parts.append(f'[white]Notes:[/] {task.description.notes}')
        scenario_parts = []
        if task.user_scenario.persona:
            scenario_parts.append(f'[white]Persona:[/] {task.user_scenario.persona}')
        scenario_parts.append(f'[white]Task Instructions:[/] {task.user_scenario.instructions}')
        if scenario_parts:
            content_parts.append('[bold cyan]User Scenario:[/]\n' + '\n'.join(scenario_parts))
        if task.initial_state:
            initial_state_parts = []
            if task.initial_state.initialization_data:
                initial_state_parts.append(f'[white]Initialization Data:[/]\n{task.initial_state.initialization_data.model_dump_json(indent=2)}')
            if task.initial_state.initialization_actions:
                initial_state_parts.append(f'[white]Initialization Actions:[/]\n{json.dumps([a.model_dump() for a in task.initial_state.initialization_actions], indent=2)}')
            if task.initial_state.message_history:
                initial_state_parts.append(f'[white]Message History:[/]\n{json.dumps([m.model_dump() for m in task.initial_state.message_history], indent=2)}')
            if initial_state_parts:
                content_parts.append('[bold cyan]Initial State:[/]\n' + '\n'.join(initial_state_parts))
        if task.evaluation_criteria:
            eval_parts = []
            if task.evaluation_criteria.actions:
                eval_parts.append(f'[white]Required Actions:[/]\n{json.dumps([a.model_dump() for a in task.evaluation_criteria.actions], indent=2)}')
            if task.evaluation_criteria.env_assertions:
                eval_parts.append(f'[white]Env Assertions:[/]\n{json.dumps([a.model_dump() for a in task.evaluation_criteria.env_assertions], indent=2)}')
            if task.evaluation_criteria.communicate_info:
                eval_parts.append(f'[white]Information to Communicate:[/]\n{json.dumps(task.evaluation_criteria.communicate_info, indent=2)}')
            if eval_parts:
                content_parts.append('[bold cyan]Evaluation Criteria:[/]\n' + '\n'.join(eval_parts))
        content = '\n\n'.join(content_parts)
        task_panel = Panel(content, title='[bold blue]Task Details', border_style='blue', expand=True)
        cls.console.print(task_panel)

    @classmethod
    def display_simulation(cls, simulation: SimulationRun, show_details: bool=True):
        """
        Display the simulation content in a formatted way using Rich library.

        Args:
            simulation: The simulation object to display
            show_details: Whether to show detailed information
        """
        sim_info = Text()
        if show_details:
            sim_info.append('Simulation ID: ', style='bold cyan')
            sim_info.append(f'{simulation.id}\n')
        sim_info.append('Task ID: ', style='bold cyan')
        sim_info.append(f'{simulation.task_id}\n')
        sim_info.append('Trial: ', style='bold cyan')
        sim_info.append(f'{simulation.trial}\n')
        if show_details:
            sim_info.append('Start Time: ', style='bold cyan')
            sim_info.append(f'{simulation.start_time}\n')
            sim_info.append('End Time: ', style='bold cyan')
            sim_info.append(f'{simulation.end_time}\n')
        sim_info.append('Duration: ', style='bold cyan')
        sim_info.append(f'{simulation.duration:.2f}s\n')
        sim_info.append('Termination Reason: ', style='bold cyan')
        sim_info.append(f'{simulation.termination_reason}\n')
        if simulation.agent_cost is not None:
            sim_info.append('Agent Cost: ', style='bold cyan')
            sim_info.append(f'${simulation.agent_cost:.4f}\n')
        if simulation.user_cost is not None:
            sim_info.append('User Cost: ', style='bold cyan')
            sim_info.append(f'${simulation.user_cost:.4f}\n')
        if simulation.reward_info:
            marker = '✅' if is_successful(simulation.reward_info.reward) else '❌'
            sim_info.append('Reward: ', style='bold cyan')
            if simulation.reward_info.reward_breakdown:
                breakdown = sorted([f'{k.value}: {v:.1f}' for k, v in simulation.reward_info.reward_breakdown.items()])
            else:
                breakdown = []
            sim_info.append(f"{marker} {simulation.reward_info.reward:.4f} ({', '.join(breakdown)})\n")
            if simulation.reward_info.db_check:
                sim_info.append('\nDB Check:', style='bold magenta')
                sim_info.append(f"{('✅' if simulation.reward_info.db_check.db_match else '❌')} {simulation.reward_info.db_check.db_reward}\n")
            if simulation.reward_info.env_assertions:
                sim_info.append('\nEnv Assertions:\n', style='bold magenta')
                for i, assertion in enumerate(simulation.reward_info.env_assertions):
                    sim_info.append(f"- {i}: {assertion.env_assertion.env_type} {assertion.env_assertion.func_name} {('✅' if assertion.met else '❌')} {assertion.reward}\n")
            if simulation.reward_info.action_checks:
                sim_info.append('\nAction Checks:\n', style='bold magenta')
                for i, check in enumerate(simulation.reward_info.action_checks):
                    sim_info.append(f"- {i}: {check.action.name} {('✅' if check.action_match else '❌')} {check.action_reward}\n")
            if simulation.reward_info.communicate_checks:
                sim_info.append('\nCommunicate Checks:\n', style='bold magenta')
                for i, check in enumerate(simulation.reward_info.communicate_checks):
                    sim_info.append(f"- {i}: {check.info} {('✅' if check.met else '❌')}\n")
            if simulation.reward_info.nl_assertions:
                sim_info.append('\nNL Assertions:\n', style='bold magenta')
                for i, assertion in enumerate(simulation.reward_info.nl_assertions):
                    sim_info.append(f"- {i}: {assertion.nl_assertion} {('✅' if assertion.met else '❌')}\n\t{assertion.justification}\n")
            if simulation.reward_info.info:
                sim_info.append('\nAdditional Info:\n', style='bold magenta')
                for key, value in simulation.reward_info.info.items():
                    sim_info.append(f'{key}: {value}\n')
        cls.console.print(Panel(sim_info, title='Simulation Overview', border_style='blue'))
        if simulation.messages:
            table = Table(title='Messages', show_header=True, header_style='bold magenta', show_lines=True)
            table.add_column('Role', style='cyan', no_wrap=True)
            table.add_column('Content', style='green')
            table.add_column('Details', style='yellow')
            table.add_column('Turn', style='yellow', no_wrap=True)
            current_turn = None
            for msg in simulation.messages:
                content = msg.content if msg.content is not None else ''
                details = ''
                if isinstance(msg, AssistantMessage):
                    role_style = 'bold blue'
                    content_style = 'blue'
                    tool_style = 'bright_blue'
                elif isinstance(msg, UserMessage):
                    role_style = 'bold green'
                    content_style = 'green'
                    tool_style = 'bright_green'
                elif isinstance(msg, ToolMessage):
                    if msg.requestor == 'user':
                        role_style = 'bold green'
                        content_style = 'bright_green'
                    else:
                        role_style = 'bold blue'
                        content_style = 'bright_blue'
                else:
                    role_style = 'bold magenta'
                    content_style = 'magenta'
                if isinstance(msg, AssistantMessage) or isinstance(msg, UserMessage):
                    if msg.tool_calls:
                        tool_calls = []
                        for tool in msg.tool_calls:
                            tool_calls.append(f'[{tool_style}]Tool: {tool.name}[/]\n[{tool_style}]Args: {json.dumps(tool.arguments, indent=2)}[/]')
                        details = '\n'.join(tool_calls)
                elif isinstance(msg, ToolMessage):
                    details = f'[{content_style}]Tool ID: {msg.id}. Requestor: {msg.requestor}[/]'
                    if msg.error:
                        details += ' [bold red](Error)[/]'
                if current_turn is not None and msg.turn_idx != current_turn:
                    table.add_row('', '', '', '')
                current_turn = msg.turn_idx
                table.add_row(f'[{role_style}]{msg.role}[/]', f'[{content_style}]{content}[/]', details, str(msg.turn_idx) if msg.turn_idx is not None else '')
            if show_details:
                cls.console.print(table)

    @classmethod
    def display_agent_metrics(cls, metrics: AgentMetrics):
        content = Text()
        content.append('🏆 Average Reward: ', style='bold cyan')
        content.append(f'{metrics.avg_reward:.4f}\n\n')
        content.append('📈 Pass^k Metrics:', style='bold cyan')
        for k, pass_hat_k in metrics.pass_hat_ks.items():
            content.append(f'\nk={k}: ', style='bold white')
            content.append(f'{pass_hat_k:.3f}')
        content.append('\n\n💰 Average Cost per Conversation: ', style='bold cyan')
        content.append(f'${metrics.avg_agent_cost:.4f}\n\n')
        metrics_panel = Panel(content, title='[bold blue]Agent Metrics', border_style='blue', expand=True)
        cls.console.print(metrics_panel)
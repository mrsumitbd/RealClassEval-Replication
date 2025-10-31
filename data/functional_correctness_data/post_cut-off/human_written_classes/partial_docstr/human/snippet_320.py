from typing import List, Optional
from tau2.data_model.tasks import Action, Task
import json
from tau2.data_model.message import AssistantMessage, Message, SystemMessage, ToolMessage, UserMessage
from tau2.data_model.simulation import RunConfig, SimulationRun

class MarkdownDisplay:

    @classmethod
    def display_actions(cls, actions: List[Action]) -> str:
        """Display actions in markdown format."""
        return f'```json\n{json.dumps([action.model_dump() for action in actions], indent=2)}\n```'

    @classmethod
    def display_messages(cls, messages: list[Message]) -> str:
        """Display messages in markdown format."""
        return '\n\n'.join((cls.display_message(msg) for msg in messages))

    @classmethod
    def display_simulation(cls, sim: SimulationRun) -> str:
        """Display simulation in markdown format."""
        output = []
        output.append(f'**Task ID**: {sim.task_id}')
        output.append(f'**Trial**: {sim.trial}')
        output.append(f'**Duration**: {sim.duration:.2f}s')
        output.append(f'**Termination**: {sim.termination_reason}')
        if sim.agent_cost is not None:
            output.append(f'**Agent Cost**: ${sim.agent_cost:.4f}')
        if sim.user_cost is not None:
            output.append(f'**User Cost**: ${sim.user_cost:.4f}')
        if sim.reward_info:
            breakdown = sorted([f'{k.value}: {v:.1f}' for k, v in sim.reward_info.reward_breakdown.items()])
            output.append(f"**Reward**: {sim.reward_info.reward:.4f} ({', '.join(breakdown)})\n")
            output.append(f'**Reward**: {sim.reward_info.reward:.4f}')
            if sim.reward_info.db_check:
                output.append('\n**DB Check**')
                output.append(f"- Status: {('✅' if sim.reward_info.db_check.db_match else '❌')} {sim.reward_info.db_check.db_reward}")
            if sim.reward_info.env_assertions:
                output.append('\n**Env Assertions**')
                for i, assertion in enumerate(sim.reward_info.env_assertions):
                    output.append(f"- {i}: {assertion.env_assertion.env_type} {assertion.env_assertion.func_name} {('✅' if assertion.met else '❌')} {assertion.reward}")
            if sim.reward_info.action_checks:
                output.append('\n**Action Checks**')
                for i, check in enumerate(sim.reward_info.action_checks):
                    output.append(f"- {i}: {check.action.name} {('✅' if check.action_match else '❌')} {check.action_reward}")
            if sim.reward_info.communicate_checks:
                output.append('\n**Communicate Checks**')
                for i, check in enumerate(sim.reward_info.communicate_checks):
                    output.append(f"- {i}: {check.info} {('✅' if check.met else '❌')} {check.justification}")
            if sim.reward_info.nl_assertions:
                output.append('\n**NL Assertions**')
                for i, assertion in enumerate(sim.reward_info.nl_assertions):
                    output.append(f"- {i}: {assertion.nl_assertion} {('✅' if assertion.met else '❌')} {assertion.justification}")
            if sim.reward_info.info:
                output.append('\n**Additional Info**')
                for key, value in sim.reward_info.info.items():
                    output.append(f'- {key}: {value}')
        if sim.messages:
            output.append('\n**Messages**:')
            output.extend((cls.display_message(msg) for msg in sim.messages))
        return '\n\n'.join(output)

    @classmethod
    def display_result(cls, task: Task, sim: SimulationRun, reward: Optional[float]=None, show_task_id: bool=False) -> str:
        """Display a single result with all its components in markdown format."""
        output = [f'## Task {task.id}' if show_task_id else '## Task', '\n### User Instruction', task.user_scenario.instructions, '\n### Ground Truth Actions', cls.display_actions(task.evaluation_criteria.actions)]
        if task.evaluation_criteria.communicate_info:
            output.extend(['\n### Communicate Info', '```\n' + str(task.evaluation_criteria.communicate_info) + '\n```'])
        if reward is not None:
            output.extend(['\n### Reward', f'**{reward:.3f}**'])
        output.extend(['\n### Simulation', cls.display_simulation(sim)])
        return '\n'.join(output)

    @classmethod
    def display_message(cls, msg: Message) -> str:
        """Display a single message in markdown format."""
        parts = []
        turn_prefix = f'[TURN {msg.turn_idx}] ' if msg.turn_idx is not None else ''
        if isinstance(msg, AssistantMessage) or isinstance(msg, UserMessage):
            parts.append(f'{turn_prefix}**{msg.role}**:')
            if msg.content:
                parts.append(msg.content)
            if msg.tool_calls:
                tool_calls = []
                for tool in msg.tool_calls:
                    tool_calls.append(f'**Tool Call**: {tool.name}\n```json\n{json.dumps(tool.arguments, indent=2)}\n```')
                parts.extend(tool_calls)
        elif isinstance(msg, ToolMessage):
            status = ' (Error)' if msg.error else ''
            parts.append(f'{turn_prefix}**tool{status}**:')
            parts.append(f'Reponse to: {msg.requestor}')
            if msg.content:
                parts.append(f'```\n{msg.content}\n```')
        elif isinstance(msg, SystemMessage):
            parts.append(f'{turn_prefix}**system**:')
            if msg.content:
                parts.append(msg.content)
        return '\n'.join(parts)
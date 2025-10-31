from tau2.data_model.tasks import RewardType, Task
from tau2.config import DEFAULT_LLM_NL_ASSERTIONS, DEFAULT_LLM_NL_ASSERTIONS_ARGS
import json
from tau2.data_model.message import Message, SystemMessage, UserMessage
from tau2.data_model.simulation import NLAssertionCheck, RewardInfo
from tau2.utils.llm_utils import generate

class NLAssertionsEvaluator:
    """
    Judge that evaluates whether a trajectory adheres to all the natural-language assertions.
    """

    @classmethod
    def calculate_reward(cls, task: Task, full_trajectory: list[Message]) -> RewardInfo:
        """
        Calculate the reward for the simulation by using an LLM to evaluate whether the trajectory adheres to all the natural-language assertions
        """
        if task.evaluation_criteria is None:
            return RewardInfo(reward=1.0, nl_assertions=[], info={'note': 'No evaluation criteria'}, reward_breakdown={RewardType.NL_ASSERTION: 1.0})
        nl_assertions = task.evaluation_criteria.nl_assertions
        if not nl_assertions:
            return RewardInfo(reward=1.0, nl_assertions=[], info={'note': 'No nl_assertions to evaluate'}, reward_breakdown={RewardType.NL_ASSERTION: 1.0})
        nl_assertions_checks = cls.evaluate_nl_assertions(full_trajectory, nl_assertions)
        all_expectations_met = all((result.met for result in nl_assertions_checks))
        reward = 1.0 if all_expectations_met else 0.0
        return RewardInfo(reward=reward, nl_assertions=nl_assertions_checks, reward_breakdown={RewardType.NL_ASSERTION: reward})

    @classmethod
    def evaluate_nl_assertions(cls, trajectory: list[Message], nl_assertions: list[str]) -> list[NLAssertionCheck]:
        """
        Evaluate whether the trajectory meets each expected outcome.

        Args:
            trajectory: List of messages from the conversation
            nl_assertions: List of natural-language assertions to evaluate

        Returns:
            List of evaluation results for each NL assertion, containing:
            - nl_assertion: The NL assertion being evaluated
            - metExpectation: Boolean indicating if the assertion was met
            - reasoning: Explanation for the evaluation
        """
        trajectory_str = '\n'.join([f'{message.role}: {message.content}' for message in trajectory])
        system_prompt = '\n        TASK\n        - You will be given a list of expected outcomes and a conversation that was collected during a test case run.\n        - The conversation is between an agent and a customer.\n        - Your job is to evaluate whether the agent satisfies each of the expected outcomes.\n        - Grade each expected outcome individually.\n\n        FORMAT\n        - Your response should be a JSON object with the following fields:\n        - `reasoning`: a short explanation for your classification\n        - `metExpectation`: `true` if the agent satisfies the expected outcomes, `false` otherwise\n        - `expectedOutcome`: repeat the expectation from the input that you are grading\n        \n        Example response structure:\n        {\n            "results": [\n                {\n                    "expectedOutcome": "<one of the expected outcomes from the input>",\n                    "reasoning": "<reasoning trace>",\n                    "metExpectation": <false or true>,\n                }\n            ]\n        }\n        '
        user_prompt = f'\n        conversation:\n        {trajectory_str}\n        \n        expectedOutcomes:\n        {nl_assertions}\n        '
        messages = [SystemMessage(role='system', content=system_prompt), UserMessage(role='user', content=user_prompt)]
        assistant_message = generate(model=DEFAULT_LLM_NL_ASSERTIONS, messages=messages, **DEFAULT_LLM_NL_ASSERTIONS_ARGS)
        result_data = json.loads(assistant_message.content)
        return [NLAssertionCheck(nl_assertion=result['expectedOutcome'], met=result['metExpectation'], justification=result['reasoning']) for result in result_data.get('results', [])]
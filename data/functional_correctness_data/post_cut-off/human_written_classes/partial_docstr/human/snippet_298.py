from syftr.studies import AgentStudyConfig, StudyConfig
from llama_index.core.evaluation.base import BaseEvaluator
from llama_index.core.prompts import ChatMessage, ChatPromptTemplate, MessageRole
import typing as T
from syftr.llm import get_llm
from llama_index.core.evaluation.correctness import CorrectnessEvaluator

class CorrectnessEvaluatorFactory:
    """Factory class to create LLM judges of type CorrectnessEvaluator based on the study configuration."""

    def __init__(self, study_config: T.Union[StudyConfig, AgentStudyConfig]):
        assert isinstance(study_config, StudyConfig), 'AgentStudyConfig needs to provide dataset information.'
        self.llm_names = study_config.evaluation.llm_names
        self.eval_type = study_config.evaluation.eval_type
        self.eval_system_template = study_config.evaluation.eval_system_template
        self.eval_user_template = study_config.dataset.eval_user_template
        self.score_threshold = study_config.evaluation.score_threshold
        assert self.eval_type == 'correctness', f"Unsupported evaluation type: {self.eval_type}. Currently only 'correctness' is supported."

    def _get_correctness_evaluators(self) -> T.List[BaseEvaluator]:
        eval_llms = [get_llm(name) for name in self.llm_names]
        eval_template = ChatPromptTemplate(message_templates=[ChatMessage(role=MessageRole.SYSTEM, content=self.eval_system_template), ChatMessage(role=MessageRole.USER, content=self.eval_user_template)])
        return [CorrectnessEvaluator(llm=llm, eval_template=eval_template, score_threshold=self.score_threshold, parser_function=json_parser_function) for llm in eval_llms]

    def get_evaluators(self) -> T.List[BaseEvaluator]:
        match self.eval_type:
            case 'correctness':
                return self._get_correctness_evaluators()
            case _:
                raise ValueError(f"Unsupported evaluation type: {self.eval_type}. Currently only 'correctness' is supported.")
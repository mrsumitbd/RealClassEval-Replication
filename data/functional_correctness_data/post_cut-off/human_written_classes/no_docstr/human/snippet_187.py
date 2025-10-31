from verdict import Layer, Pipeline
from verdict.scale import ContinuousScale, DiscreteScale
from verdict.schema import Schema
from verdict.transform import MaxPoolUnit
from verdict.common.judge import CategoricalJudgeUnit, JudgeUnit

class OptimizerEvaluator:

    def __init__(self):
        self.score_pipeline = Pipeline() >> Layer(JudgeUnit(scale=ContinuousScale(1, 10)).prompt('You are a judge that is an expert at evaluating optimizers for their novelty as they will be accepted to a prestigious research conference. Given the following optimizer code and its architecture/use-case, you must rate it on a scale of 1 to 10 based on how novel it is and its impactfulness in speeding up model training. Here is the code: {source.optimizer_code}\nHere is the architecture: {source.architecture}'), repeat=3).via('xai/grok-3-latest') >> MaxPoolUnit()
        self.validity_pipeline = Pipeline() >> Layer(CategoricalJudgeUnit(name='Judge', categories=DiscreteScale(['yes', 'no']), explanation=False).prompt('\n                    You are an expert code validator specializing in PyTorch optimizers.\n                    Your task is to determine if the provided optimizer code is completely valid and error-free.\n\n                    A valid optimizer MUST satisfy ALL of these criteria:\n                    1. Has zero syntax or runtime errors:\n                       - No undefined variables\n                       - No type mismatches\n                       - No memory issues\n                       - No CUDA/CPU compatibility problems\n                    2. Can be imported and instantiated without blocking errors\n                    3. Can run a complete optimization step without exceptions\n\n                    Optimizer Code: {source.optimizer_code}\n                    Stdout: {source.stdout}\n                    Stderr: {source.stderr}\n\n                    Respond with:\n                    - "yes" if ALL criteria are met and the code is completely error-free\n                    - "no" if ANY criterion fails or there are ANY potential issues\n\n                    Be extremely strict in your evaluation.\n                ').via('xai/grok-3-latest', retries=2))

    def score(self, optimizer_code: str, architecture: str) -> int:
        schema = Schema.of(optimizer_code=optimizer_code, architecture=architecture)
        response, _ = self.score_pipeline.run(schema)
        return response.get('Pipeline_root.block.block.unit[Map MaxPool]_score', 0.0)

    def check_validity(self, optimizer_code: str, stdout: str, stderr: str) -> bool:
        schema = Schema.of(optimizer_code=optimizer_code, stdout=stdout, stderr=stderr)
        response, _ = self.validity_pipeline.run(schema)
        choice = response.get('Pipeline_root.block.layer[0].unit[CategoricalJudge Judge]_choice', None)
        return choice == 'yes'
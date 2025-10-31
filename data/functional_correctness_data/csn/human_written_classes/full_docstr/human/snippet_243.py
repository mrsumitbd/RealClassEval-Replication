import logging
from workbench.api import DataSource, FeatureSet, Model, Endpoint
from workbench.api.model import ModelType

class PipelineExecutor:
    """PipelineExecutor: Internal Class: Executes a Workbench Pipeline

    Common Usage:
        ```python
        my_pipeline = PipelineExecutor(pipeline)
        my_pipeline.execute()  # Execute entire pipeline
        my_pipeline.execute_partial(["data_source", "feature_set"])
        my_pipeline.execute_partial(["model", "endpoint"])
        ```
    """

    def __init__(self, pipeline):
        """PipelineExecutor Init Method"""
        self.log = logging.getLogger('workbench')
        self.pipeline_name = pipeline.name
        self.pipeline = pipeline.pipeline

    def execute(self, subset: list=None):
        """Execute the Workbench Pipeline

        Args:
            subset (list): A list of steps to execute. If None, execute the entire pipeline

        Raises:
            RuntimeError: If the pipeline execution fails in any way
        """
        self.log.important(f'Executing Pipeline {self.pipeline_name}...')
        if subset:
            self.log.important(f'\tSubset: {subset}')
        workbench_objects = {}
        for class_name, kwargs in self.pipeline.items():
            data_input = kwargs['input']
            del kwargs['input']
            if isinstance(input, str) and data_input == '<<parameter_required>>':
                msg = 'Call set_input() to set the input (DataFrame, file path or S3 path)'
                self.log.critical(msg)
                raise RuntimeError(msg)
            if class_name == 'data_source':
                if not subset or 'data_source' in subset:
                    workbench_objects['data_source'] = DataSource(data_input, **kwargs)
                else:
                    workbench_objects['data_source'] = DataSource(source=kwargs['name'])
            elif class_name == 'feature_set':
                holdout_ids = None
                if 'holdout_ids' in kwargs:
                    if kwargs['holdout_ids'] == '<<parameter_optional>>':
                        self.log.important('Hold out ids are not set, defaulting to 80/20 split')
                        holdout_ids = None
                        id_column = None
                    else:
                        holdout_ids = kwargs['holdout_ids']
                        if 'id_column' not in kwargs or kwargs['id_column'] == '<<parameter_optional>>':
                            self.log.warning('Hold out ids are set, but no id column is provided! Defaulting to 80/20 split')
                            holdout_ids = None
                            id_column = None
                        else:
                            id_column = kwargs['id_column']
                            del kwargs['id_column']
                    del kwargs['holdout_ids']
                if 'data_source' in workbench_objects and (not subset or 'feature_set' in subset):
                    if 'feature_schema' in kwargs:
                        if kwargs['feature_schema'] == 'molecular_descriptors_v1':
                            del kwargs['feature_schema']
                            self.log.error('Feature Schema: molecular_descriptors_v1 not currently implemented')
                        else:
                            raise RuntimeError(f"Unsupported feature schema: {kwargs['feature_schema']}")
                    else:
                        workbench_objects['data_source'].to_features(**kwargs)
                workbench_objects['feature_set'] = FeatureSet(kwargs['name'])
                if holdout_ids:
                    workbench_objects['feature_set'].set_training_holdouts(id_column, holdout_ids)
            elif class_name == 'model':
                if 'model_type' in kwargs:
                    kwargs['model_type'] = ModelType(kwargs['model_type'])
                if 'feature_set' in workbench_objects and (not subset or 'model' in subset):
                    workbench_objects['feature_set'].to_model(**kwargs)
                if not subset or 'endpoint' in subset:
                    workbench_objects['model'] = Model(kwargs['name'])
                    workbench_objects['model'].set_owner('pipeline')
            elif class_name == 'endpoint':
                if 'model' in workbench_objects and (not subset or 'endpoint' in subset):
                    workbench_objects['model'].to_endpoint(**kwargs)
                    endpoint = Endpoint(kwargs['name'])
                    endpoint.auto_inference(capture=True)
            else:
                raise RuntimeError(f'Unsupported pipeline stage: {class_name}')

    def execute_partial(self, subset: list):
        """Execute a partial Pipeline

        Args:
            subset (list): A subset of the pipeline to execute

        Raises:
            RunTimeException: If the pipeline execution fails in any way
        """
        self.execute(subset)
import yaml
from loguru import logger
import os
from typing import Any, Dict, Optional, Tuple
import json

class EnvironmentConfigLoader:
    """
    Loads environment configurations from configuration files (YAML/JSON) and creates RayEnvironmentActor instances.
    """

    def __init__(self):
        pass

    @staticmethod
    def load_environments_from_file(file_path: str) -> Dict[int, 'ray.actor.ActorHandle']:
        """
        Loads all environment definitions from the specified configuration file and starts a RayEnvironmentActor for each definition.
        Args:
            file_path: The path to the YAML or JSON configuration file.
        Returns:
            A dictionary mapping env_id to the corresponding RayEnvironmentActor handle.
        """
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()
        raw_configs = None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_extension in ['.yaml', '.yml']:
                    raw_configs_list = yaml.safe_load(f)
                elif file_extension == '.json':
                    raw_configs_list = json.load(f)
                else:
                    raise ValueError(f'Unsupported configuration file extension: {file_extension}')
            if not isinstance(raw_configs_list, list):
                raise ValueError('The environment configuration file should contain a list of environment configuration objects.')
        except Exception as e:
            logger.info(f"Error: Failed to load or parse environment configuration file '{file_path}': {e}")
            raise
        environment_actors: Dict[int, 'ray.actor.ActorHandle'] = {}
        for env_conf in raw_configs_list:
            env_id = env_conf.get('environment_id', None)
            env_class_ref = env_conf.get('environment_type_ref', None)
            env_specific_config = env_conf.get('config', {})
            ray_actor_options = env_conf.get('source_options', {})
            if env_id is None or env_class_ref is None:
                logger.info(f'Warning: Skipping invalid environment configuration (missing id or type_ref): {env_conf}')
                continue
            try:
                agent_parallel_num = env_conf.get('agent_parallel_num', 1)
                n_agent = env_specific_config.get('num_agents', 1)
                if agent_parallel_num > 1 and n_agent > 1:
                    actor_handle = ParallelRayEnvRunner.options(**ray_actor_options).remote(env_id=env_id, agent_parallel_num=min(agent_parallel_num, n_agent), env_class_ref=env_class_ref, env_config=env_specific_config)
                    environment_actors[env_id] = actor_handle
                    logger.info(f"Successfully started RayEnvironmentActor for env_id='{env_id}' (type: {env_class_ref}).")
                else:
                    actor_handle = RayEnvRunner.options(**ray_actor_options).remote(env_id=env_id, env_class_ref=env_class_ref, env_config=env_specific_config)
                    environment_actors[env_id] = actor_handle
                    logger.info(f"Successfully started RayEnvironmentActor for env_id='{env_id}' (type: {env_class_ref}).")
            except Exception as e:
                logger.info(f"Error: Failed to start RayEnvironmentActor for env_id='{env_id}': {e}")
        return environment_actors
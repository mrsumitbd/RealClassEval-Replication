import traceback
from metasim.scenario.scenario import ScenarioCfg
from metasim.constants import SimType
from metasim.utils.setup_util import get_sim_handler_class
from metasim.sim.base import BaseSimHandler
from loguru import logger as log

class HandlerContext:

    def __init__(self, scenario: ScenarioCfg):
        self.scenario = scenario
        self.handler = get_sim_handler_class(SimType(self.scenario.simulator))(scenario)

    def __enter__(self) -> BaseSimHandler:
        if self.scenario.simulator == 'isaaclab':
            global _is_first_isaaclab_context
            if _is_first_isaaclab_context:
                _is_first_isaaclab_context = False
                self.handler.launch()
            else:
                try:
                    from omni.isaac.core.utils.stage import create_new_stage
                except ModuleNotFoundError:
                    from isaacsim.core.utils.stage import create_new_stage
                create_new_stage()
                self.handler._setup_environment()
        else:
            self.handler.launch()
        return self.handler

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            log.error('Error in SimContext:')
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        self.handler.close()
from vivarium.framework.lifecycle import LifeCycleInterface, LifeCycleManager, lifecycle_states
from layered_config_tree.main import LayeredConfigTree
from vivarium.framework.values import ValuesInterface, ValuesManager
from vivarium.framework.time import SimulationClock, TimeInterface
from vivarium.framework.randomness import RandomnessInterface, RandomnessManager
from vivarium.framework.population import PopulationInterface, PopulationManager
from vivarium.framework.components import ComponentConfigError, ComponentInterface, ComponentManager
from vivarium.framework.logging import LoggingInterface, LoggingManager
from vivarium.framework.artifact import ArtifactInterface, ArtifactManager
from vivarium.framework.resource import ResourceInterface, ResourceManager
from vivarium.framework.event import EventInterface, EventManager
from vivarium.framework.lookup import LookupTableInterface, LookupTableManager
from vivarium.framework.plugins import PluginManager
from vivarium.framework.results import ResultsInterface, ResultsManager

class Builder:
    """Toolbox for constructing and configuring simulation components.

    This is the access point for components through which they are able to
    utilize a variety of interfaces to interact with the simulation framework.

    Notes
    -----
    A `Builder` should never be created directly. It will automatically be
    created during the initialization of a :class:`SimulationContext`

    """

    def __init__(self, configuration: LayeredConfigTree, plugin_manager: PluginManager) -> None:
        self.configuration = configuration
        'Provides access to the :ref:`configuration<configuration_concept>`'
        self.logging = plugin_manager.get_plugin_interface(LoggingInterface)
        'Provides access to the :ref:`logging<logging_concept>` system.'
        self.lookup = plugin_manager.get_plugin_interface(LookupTableInterface)
        'Provides access to simulant-specific data via the\n        :ref:`lookup table<lookup_concept>` abstraction.'
        self.value = plugin_manager.get_plugin_interface(ValuesInterface)
        'Provides access to computed simulant attribute values via the\n        :ref:`value pipeline<values_concept>` system.'
        self.event = plugin_manager.get_plugin_interface(EventInterface)
        'Provides access to event listeners utilized in the\n        :ref:`event<event_concept>` system.'
        self.population = plugin_manager.get_plugin_interface(PopulationInterface)
        'Provides access to simulant state table via the\n        :ref:`population<population_concept>` system.'
        self.resources = plugin_manager.get_plugin_interface(ResourceInterface)
        'Provides access to the :ref:`resource<resource_concept>` system,\n         which manages dependencies between components.\n         '
        self.results = plugin_manager.get_plugin_interface(ResultsInterface)
        'Provides access to the :ref:`results<results_concept>` system.'
        self.randomness = plugin_manager.get_plugin_interface(RandomnessInterface)
        'Provides access to the :ref:`randomness<crn_concept>` system.'
        self.time: TimeInterface = plugin_manager.get_plugin_interface(TimeInterface)
        "Provides access to the simulation's :ref:`clock<time_concept>`."
        self.components = plugin_manager.get_plugin_interface(ComponentInterface)
        'Provides access to the :ref:`component management<components_concept>`\n        system, which maintains a reference to all managers and components in\n        the simulation.'
        self.lifecycle = plugin_manager.get_plugin_interface(LifeCycleInterface)
        "Provides access to the :ref:`life-cycle<lifecycle_concept>` system,\n        which manages the simulation's execution life-cycle."
        self.data = plugin_manager.get_plugin_interface(ArtifactInterface)
        "Provides access to the simulation's input data housed in the\n        :ref:`data artifact<data_concept>`."
        for name, interface in plugin_manager.get_optional_interfaces().items():
            setattr(self, name, interface)

    def __repr__(self) -> str:
        return 'Builder()'
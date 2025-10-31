
class BaziManager:
    """
    A simple manager for Bazi tools and their properties.
    """

    def __init__(self):
        """
        Initialize the manager with an empty registry of tools.
        """
        self.tools = {}

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
        Register tools based on a list of property names.

        Parameters
        ----------
        add_tool : callable or None
            A callable that accepts two arguments (tool_name, property_instance).
            If None, the tool will not be added via this callback.
        PropertyList : Iterable[str]
            An iterable of property names to register.
        Property : type
            A class or callable that creates a property instance.
            It should accept at least two arguments: name and type.
        PropertyType : type
            The type to associate with each property.

        Returns
        -------
        None
        """
        # Ensure we have a fresh registry
        self.tools = {}

        # Iterate over the provided property names
        for name in PropertyList:
            # Create a property instance
            prop_instance = Property(name, PropertyType)

            # Store it in the internal registry
            self.tools[name] = prop_instance

            # If a callback is provided, invoke it
            if callable(add_tool):
                try:
                    add_tool(name, prop_instance)
                except Exception:
                    # Silently ignore errors from the callback to avoid breaking the loop
                    pass

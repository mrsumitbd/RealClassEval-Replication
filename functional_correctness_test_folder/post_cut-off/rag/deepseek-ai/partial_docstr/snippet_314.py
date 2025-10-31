
class DiscoveryMixin:
    '''
    Mixin class for BedrockServerManager that handles server discovery and validation.
    '''

    def validate_server(self, server_name: str, app_context: Optional[AppContext] = None) -> bool:
        '''Validates if a given server name corresponds to a valid installation.
        This method checks for the existence and basic integrity of a server
        installation. It instantiates a :class:`~.core.bedrock_server.BedrockServer`
        object for the given ``server_name`` and then calls its
        :meth:`~.core.bedrock_server.BedrockServer.is_installed` method.
        Any exceptions raised during the instantiation or validation process (e.g.,
        :class:`~.error.InvalidServerNameError`, :class:`~.error.ConfigurationError`)
        are caught, logged as a warning, and result in a ``False`` return value,
        making this a safe check.
        Args:
            server_name (str): The name of the server to validate. This should
                correspond to a subdirectory within the main server base directory.
        Returns:
            bool: ``True`` if the server exists and is a valid installation
            (i.e., its directory and executable are found), ``False`` otherwise.
        Raises:
            MissingArgumentError: If ``server_name`` is an empty string.
        '''
        if not server_name:
            raise MissingArgumentError("server_name cannot be empty")
        try:
            server = BedrockServer(server_name, app_context)
            return server.is_installed()
        except (InvalidServerNameError, ConfigurationError) as e:
            logging.warning(
                f"Validation failed for server {server_name}: {str(e)}")
            return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        '''Discovers and retrieves status data for all valid server instances.
        This method scans the main server base directory (defined by
        ``settings['paths.servers']``) for subdirectories that represent server
        installations. For each potential server, it:
            1. Instantiates a :class:`~.core.bedrock_server.BedrockServer` object.
            2. Validates the installation using the server's :meth:`~.core.bedrock_server.BedrockServer.is_installed` method.
            3. If valid, it queries the server's status and version using
               :meth:`~.core.bedrock_server.BedrockServer.get_status` and
               :meth:`~.core.bedrock_server.BedrockServer.get_version`.
        Errors encountered while processing individual servers are collected and
        returned separately, allowing the method to succeed even if some server
        directories are corrupted or misconfigured. The final list of server
        data is sorted alphabetically by server name.
        Returns:
            Tuple[List[Dict[str, Any]], List[str]]: A tuple containing two lists:
                - The first list contains dictionaries, one for each successfully
                  processed server. Each dictionary has the keys:
                    - ``"name"`` (str): The name of the server.
                    - ``"status"`` (str): The server's current status (e.g., "RUNNING", "STOPPED").
                    - ``"version"`` (str): The detected version of the server.
                - The second list contains string messages describing any errors that
                  occurred while processing specific server candidates.
        Raises:
            AppFileNotFoundError: If the main server base directory
                (``settings['paths.servers']``) is not configured or does not exist.
        '''
        servers_data = []
        errors = []
        servers_dir = settings.get('paths.servers')
        if not servers_dir or not os.path.isdir(servers_dir):
            raise AppFileNotFoundError(
                "Server base directory not found or not configured")

        for server_name in os.listdir(servers_dir):
            server_path = os.path.join(servers_dir, server_name)
            if not os.path.isdir(server_path):
                continue
            try:
                server = BedrockServer(server_name, app_context)
                if not server.is_installed():
                    errors.append(
                        f"Server {server_name} is not a valid installation")
                    continue
                status = server.get_status()
                version = server.get_version()
                servers_data.append({
                    "name": server_name,
                    "status": status,
                    "version": version
                })
            except Exception as e:
                errors.append(
                    f"Error processing server {server_name}: {str(e)}")

        servers_data.sort(key=lambda x: x["name"])
        return servers_data, errors

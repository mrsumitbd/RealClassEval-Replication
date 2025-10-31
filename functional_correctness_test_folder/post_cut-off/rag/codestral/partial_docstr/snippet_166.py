
class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.args = args
        self.model_name = args.model_name
        self.max_tokens = args.max_tokens
        self.temperature = args.temperature
        self.top_p = args.top_p
        self.top_k = args.top_k
        self.repetition_penalty = args.repetition_penalty
        self.max_history = args.max_history
        self.system_prompt = args.system_prompt
        self.user_prompt = args.user_prompt
        self.assistant_prompt = args.assistant_prompt
        self.api_key = args.api_key
        self.api_base = args.api_base
        self.api_version = args.api_version
        self.deployment_name = args.deployment_name
        self.embedding_model_name = args.embedding_model_name
        self.embedding_deployment_name = args.embedding_deployment_name
        self.search_index_name = args.search_index_name
        self.search_service_endpoint = args.search_service_endpoint
        self.search_api_key = args.search_api_key
        self.search_api_version = args.search_api_version
        self.search_top_k = args.search_top_k
        self.search_threshold = args.search_threshold
        self.search_fields = args.search_fields
        self.search_filter = args.search_filter
        self.search_strictness = args.search_strictness
        self.search_enable_in_domain = args.search_enable_in_domain
        self.search_enable_hybrid = args.search_enable_hybrid
        self.search_semantic_configuration = args.search_semantic_configuration
        self.search_query_type = args.search_query_type
        self.search_query_language = args.search_query_language
        self.search_speller_mode = args.search_speller_mode
        self.search_captions = args.search_captions
        self.search_answer = args.search_answer
        self.search_enable_semantic_ranking = args.search_enable_semantic_ranking
        self.search_enable_vector_search = args.search_enable_vector_search
        self.search_enable_hybrid_search = args.search_enable_hybrid_search
        self.search_enable_facets = args.search_enable_facets
        self.search_facets = args.search_facets
        self.search_enable_highlighting = args.search_enable_highlighting
        self.search_highlighting_pre_tag = args.search_highlighting_pre_tag
        self.search_highlighting_post_tag = args.search_highlighting_post_tag
        self.search_enable_semantic_captions = args.search_enable_semantic_captions
        self.search_enable_query_answer = args.search_enable_query_answer
        self.search_enable_query_intent = args.search_enable_query_intent
        self.search_enable_answers = args.search_enable_answers
        self.search_enable_answers_extraction = args.search_enable_answers_extraction
        self.search_enable_answers_highlighting = args.search_enable_answers_highlighting
        self.search_enable_answers_suggestions = args.search_enable_answers_suggestions
        self.search_enable_answers_visualization = args.search_enable_answers_visualization
        self.search_enable_answers_visualization_type = args.search_enable_answers_visualization_type
        self.search_enable_answers_visualization_options = args.search_enable_answers_visualization_options
        self.search_enable_answers_visualization_data = args.search_enable_answers_visualization_data
        self.search_enable_answers_visualization_data_type = args.search_enable_answers_visualization_data_type
        self.search_enable_answers_visualization_data_options = args.search_enable_answers_visualization_data_options
        self.search_enable_answers_visualization_data_data = args.search_enable_answers_visualization_data_data
        self.search_enable_answers_visualization_data_data_type = args.search_enable_answers_visualization_data_data_type
        self.search_enable_answers_visualization_data_data_options = args.search_enable_answers_visualization_data_data_options
        self.search_enable_answers_visualization_data_data_data = args.search_enable_answers_visualization_data_data_data
        self.search_enable_answers_visualization_data_data_data_type = args.search_enable_answers_visualization_data_data_data_type
        self.search_enable_answers_visualization_data_data_data_options = args.search_enable_answers_visualization_data_data_data_options

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        if not self.model_name:
            raise ValueError("Model name is required.")
        if self.max_tokens <= 0:
            raise ValueError("Max tokens must be a positive integer.")
        if not 0 <= self.temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1.")
        if not 0 <= self.top_p <= 1:
            raise ValueError("Top-p must be between 0 and 1.")
        if self.top_k <= 0:
            raise ValueError("Top-k must be a positive integer.")
        if self.repetition_penalty <= 0:
            raise ValueError("Repetition penalty must be a positive number.")
        if self.max_history < 0:
            raise ValueError("Max history must be a non-negative integer.")
        if not self.api_key:
            raise ValueError("API key is required.")
        if not self.api_base:
            raise ValueError("API base URL is required.")
        if not self.deployment_name:
            raise ValueError("Deployment name is required.")
        if not self.embedding_model_name:
            raise ValueError("Embedding model name is required.")
        if not self.embedding_deployment_name:
            raise ValueError("Embedding deployment name is required.")
        if not self.search_index_name:
            raise ValueError("Search index name is required.")
        if not self.search_service_endpoint:
            raise ValueError("Search service endpoint is required.")
        if not self.search_api_key:
            raise ValueError("Search API key is required.")
        if self.search_top_k <= 0:
            raise ValueError("Search top-k must be a positive integer.")
        if not 0 <= self.search_threshold <= 1:
            raise ValueError("Search threshold must be between 0 and 1.")
        if not self.search_fields:
            raise ValueError("Search fields are required.")
        if self.search_strictness < 0:
            raise ValueError(
                "Search strictness must be a non-negative integer.")

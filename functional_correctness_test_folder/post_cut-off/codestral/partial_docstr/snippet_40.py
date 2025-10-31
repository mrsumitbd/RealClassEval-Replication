
class SessionCalculator:

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        self.cost_limit = 100.0

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        time_data = {}
        start_time = session_data.get('start_time')
        if start_time:
            time_data['elapsed_time'] = (
                current_time - start_time).total_seconds() / 3600  # in hours
        else:
            time_data['elapsed_time'] = 0.0
        return time_data

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        '''Calculate cost-related predictions.
        Args:
            session_data: Dictionary containing session cost information
            time_data: Time data from calculate_time_data
            cost_limit: Optional cost limit (defaults to 100.0)
        Returns:
            Dictionary with cost predictions
        '''
        if cost_limit is not None:
            self.cost_limit = cost_limit
        cost_predictions = {}
        cost_rate = session_data.get('cost_rate', 0.0)
        cost_predictions['current_cost'] = cost_rate * \
            time_data['elapsed_time']
        cost_predictions['remaining_cost'] = self.cost_limit - \
            cost_predictions['current_cost']
        cost_predictions['remaining_time'] = cost_predictions['remaining_cost'] / \
            cost_rate if cost_rate > 0 else float('inf')
        return cost_predictions


class SessionCalculator:
    '''Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)'''

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        self.cost_limit_default = 100.0

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        '''Calculate time-related data for the session.
        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time
        Returns:
            Dictionary with calculated time data
        '''
        time_data = {}
        start_time = session_data.get('start_time')
        end_time = session_data.get('end_time')

        if start_time:
            time_data['duration'] = (
                current_time - start_time).total_seconds() / 3600  # in hours
            time_data['start_time'] = start_time.strftime('%Y-%m-%d %H:%M:%S')

        if end_time:
            time_data['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')

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
        cost_predictions = {}
        cost_limit = cost_limit if cost_limit is not None else self.cost_limit_default
        cost_predictions['cost_limit'] = cost_limit

        if 'duration' in time_data:
            cost_rate = session_data.get('cost_rate', 0.0)
            predicted_cost = cost_rate * time_data['duration']
            cost_predictions['predicted_cost'] = predicted_cost
            cost_predictions['cost_exceeded'] = predicted_cost > cost_limit

        return cost_predictions

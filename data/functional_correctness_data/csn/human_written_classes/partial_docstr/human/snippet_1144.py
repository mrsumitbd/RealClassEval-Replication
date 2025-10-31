from typing import Optional

class ProjectSettings:

    def __init__(self, is_collect_db_stats: Optional[bool]=None, is_data_explorer: Optional[bool]=None, is_performance_advisor: Optional[bool]=None, is_realtime_perf: Optional[bool]=None, is_schema_advisor: Optional[bool]=None):
        """Holds Project/Group settings.

        Args:
            is_collect_db_stats (Optional[bool]): Flag that indicates whether statistics in cluster metrics collection is enabled for the project.
            is_data_explorer (Optional[bool]): Flag that indicates whether Data Explorer is enabled for the project. If enabled, you can query your database with an easy to use interface.
            is_performance_advisor (Optional[bool]): Flag that indicates whether Performance Advisor and Profiler is enabled for the project. If enabled, you can analyze database logs to recommend performance improvements.
            is_realtime_perf (Optional[bool]): Flag that indicates whether Real Time Performance Panel is enabled for the project. If enabled, you can see real time metrics from your MongoDB database.
            is_schema_advisor (Optional[bool]): Flag that indicates whether Schema Advisor is enabled for the project. If enabled, you receive customized recommendations to optimize your data model and enhance performance.
        """
        self.is_schema_advisor: Optional[bool] = is_schema_advisor
        self.is_realtime_perf: Optional[bool] = is_realtime_perf
        self.is_performance_advisor: Optional[bool] = is_performance_advisor
        self.is_data_explorer: Optional[bool] = is_data_explorer
        self.is_collect_db_stats: Optional[bool] = is_collect_db_stats

    @classmethod
    def from_dict(cls, data_dict: dict):
        return cls(bool(data_dict.get('isCollectDatabaseSpecificsStatisticsEnabled', False)), bool(data_dict.get('isDataExplorerEnabled', False)), bool(data_dict.get('isPerformanceAdvisorEnabled', False)), bool(data_dict.get('isRealtimePerformancePanelEnabled', False)), bool(data_dict.get('isSchemaAdvisorEnabled', False)))
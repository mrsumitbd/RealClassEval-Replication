from typing import Any
from datetime import datetime

class MetricsCollector:
    """Collects and analyzes coordination metrics."""

    def __init__(self):
        self.metrics = CoordinationMetrics()
        self.event_log: list[dict[str, Any]] = []
        self.start_time = datetime.now()

    def log_event(self, event_type: str, data: dict[str, Any]):
        """Log a coordination event for analysis."""
        event = {'timestamp': datetime.now().isoformat(), 'type': event_type, 'data': data}
        self.event_log.append(event)
        if event_type == 'task_submitted':
            self.metrics.total_tasks_submitted += 1
        elif event_type == 'duplicate_detected':
            self.metrics.duplicate_tasks_detected += 1
            time_saved = data.get('estimated_time_saved', 0)
            self.metrics.deduplication_time_saved += time_saved
        elif event_type == 'context_shared':
            self.metrics.contexts_shared += 1
        elif event_type == 'context_inherited':
            self.metrics.contexts_inherited += 1
        elif event_type == 'file_conflict_detected':
            self.metrics.file_conflicts_detected += 1
        elif event_type == 'file_conflict_prevented':
            self.metrics.file_conflicts_prevented += 1
        elif event_type == 'pattern_suggested':
            pattern = data.get('pattern', 'unknown')
            self.metrics.patterns_suggested[pattern] = self.metrics.patterns_suggested.get(pattern, 0) + 1
        elif event_type == 'task_completed':
            self.metrics.tasks_completed_successfully += 1
            completion_time = data.get('duration', 0)
            total = self.metrics.tasks_completed_successfully
            current_avg = self.metrics.avg_task_completion_time
            self.metrics.avg_task_completion_time = (current_avg * (total - 1) + completion_time) / total

    def calculate_effectiveness_score(self) -> dict[str, Any]:
        """Calculate overall coordination effectiveness score."""
        dedup_score = 0
        if self.metrics.total_tasks_submitted > 0:
            dedup_rate = self.metrics.duplicate_tasks_detected / self.metrics.total_tasks_submitted
            dedup_score = min(100, dedup_rate * 200)
        context_score = 0
        if self.metrics.contexts_shared > 0:
            reuse_rate = self.metrics.contexts_inherited / max(1, self.metrics.contexts_shared)
            context_score = min(100, reuse_rate * 100)
        conflict_score = 0
        if self.metrics.file_conflicts_detected > 0:
            prevention_rate = self.metrics.file_conflicts_prevented / self.metrics.file_conflicts_detected
            conflict_score = prevention_rate * 100
        success_score = 0
        total_tasks = self.metrics.tasks_completed_successfully + self.metrics.tasks_failed
        if total_tasks > 0:
            success_rate = self.metrics.tasks_completed_successfully / total_tasks
            success_score = success_rate * 100
        comm_score = 0
        if self.metrics.messages_broadcast > 0:
            action_rate = self.metrics.messages_acted_upon / self.metrics.messages_broadcast
            comm_score = min(100, action_rate * 150)
        weights = {'deduplication': 0.2, 'context_sharing': 0.25, 'conflict_prevention': 0.2, 'task_success': 0.2, 'communication': 0.15}
        overall_score = dedup_score * weights['deduplication'] + context_score * weights['context_sharing'] + conflict_score * weights['conflict_prevention'] + success_score * weights['task_success'] + comm_score * weights['communication']
        return {'overall_score': round(overall_score, 2), 'deduplication_score': round(dedup_score, 2), 'context_sharing_score': round(context_score, 2), 'conflict_prevention_score': round(conflict_score, 2), 'task_success_score': round(success_score, 2), 'communication_score': round(comm_score, 2), 'weights': weights}

    def generate_report(self) -> dict[str, Any]:
        """Generate comprehensive metrics report."""
        runtime = (datetime.now() - self.start_time).total_seconds()
        effectiveness = self.calculate_effectiveness_score()
        return {'summary': {'runtime_seconds': runtime, 'overall_effectiveness': effectiveness['overall_score'], 'total_events': len(self.event_log), 'tasks_processed': self.metrics.total_tasks_submitted, 'agents_coordinated': self.metrics.agent_interaction_count}, 'effectiveness_scores': effectiveness, 'detailed_metrics': {'deduplication': {'duplicates_detected': self.metrics.duplicate_tasks_detected, 'time_saved_seconds': self.metrics.deduplication_time_saved, 'efficiency_gain': f'{self.metrics.duplicate_tasks_detected / max(1, self.metrics.total_tasks_submitted) * 100:.1f}%'}, 'context_sharing': {'contexts_shared': self.metrics.contexts_shared, 'contexts_reused': self.metrics.contexts_inherited, 'reuse_rate': f'{self.metrics.context_reuse_rate * 100:.1f}%'}, 'conflict_prevention': {'conflicts_detected': self.metrics.file_conflicts_detected, 'conflicts_prevented': self.metrics.file_conflicts_prevented, 'prevention_rate': f'{self.metrics.file_conflicts_prevented / max(1, self.metrics.file_conflicts_detected) * 100:.1f}%'}, 'performance': {'avg_task_time': f'{self.metrics.avg_task_completion_time:.2f}s', 'success_rate': f'{self.metrics.tasks_completed_successfully / max(1, self.metrics.total_tasks_submitted) * 100:.1f}%', 'parallel_execution_rate': f'{self.metrics.parallel_execution_rate * 100:.1f}%'}, 'thinking_patterns': {'most_suggested': max(self.metrics.patterns_suggested.items(), key=lambda x: x[1])[0] if self.metrics.patterns_suggested else 'none', 'pattern_distribution': self.metrics.patterns_suggested, 'pattern_success_rates': self.metrics.pattern_success_rate}}, 'recommendations': self._generate_recommendations(effectiveness)}

    def _generate_recommendations(self, effectiveness: dict[str, Any]) -> list[str]:
        """Generate recommendations based on metrics."""
        recommendations = []
        if effectiveness['deduplication_score'] < 50:
            recommendations.append('Consider improving task hashing algorithm for better deduplication')
        if effectiveness['context_sharing_score'] < 60:
            recommendations.append('Increase context relevance scoring to improve reuse')
        if effectiveness['conflict_prevention_score'] < 70:
            recommendations.append('Implement predictive conflict detection based on task descriptions')
        if effectiveness['communication_score'] < 50:
            recommendations.append('Improve message filtering to reduce noise and increase action rate')
        if self.metrics.avg_coordination_overhead > 0.15:
            recommendations.append('Coordination overhead is high (>15%), consider optimizing message passing')
        return recommendations if recommendations else ['System performing optimally']
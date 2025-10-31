import time

class StartupProfiler:
    """Detailed startup profiling with bottleneck identification."""

    def __init__(self):
        """Initialize the profiler."""
        self.profile_data: list[tuple[str, float]] = []
        self.start_time = time.perf_counter()

    def checkpoint(self, name: str):
        """Record a timing checkpoint."""
        current_time = time.perf_counter()
        elapsed = current_time - self.start_time
        self.profile_data.append((name, elapsed))

    def get_report(self) -> dict[str, float]:
        """Get a performance report showing time deltas."""
        report = {}
        prev_time = 0.0
        for name, total_time in self.profile_data:
            delta = total_time - prev_time
            report[f'{name}_total'] = total_time
            report[f'{name}_delta'] = delta
            prev_time = total_time
        return report

    def analyze_bottlenecks(self, report: dict[str, float]) -> list[str]:
        """Analyze the report and identify performance bottlenecks."""
        issues = []
        recommendations = []
        commands_time = report.get('commands_import_delta', 0)
        if commands_time > 0.5:
            issues.append(f'🚨 CRITICAL: Commands import took {commands_time:.3f}s (>0.5s)')
            recommendations.append('Commands are importing Google ADK at module level. Apply TYPE_CHECKING optimization.')
        elif commands_time > 0.1:
            issues.append(f'⚠️  WARNING: Commands import took {commands_time:.3f}s (>0.1s)')
            recommendations.append('Commands import is slower than expected. Check for heavy imports in streetrace/commands/definitions/')
        total_time = report.get('app_created_total', 0)
        if total_time > 2.0:
            issues.append(f'🚨 CRITICAL: Total startup took {total_time:.3f}s (>2.0s)')
            recommendations.append('Startup time is unacceptably slow. Focus on the largest time deltas.')
        elif total_time > 1.0:
            issues.append(f'⚠️  WARNING: Total startup took {total_time:.3f}s (>1.0s)')
            recommendations.append('Startup time is slower than target. Consider lazy loading deps.')
        app_import_time = report.get('app_import_delta', 0)
        if app_import_time > 0.5:
            issues.append(f'🚨 CRITICAL: App import took {app_import_time:.3f}s (>0.5s)')
            recommendations.append('App import is very slow. Check for expensive imports.')
        basic_imports_time = report.get('basic_imports_delta', 0)
        if basic_imports_time > 0.05:
            issues.append(f'⚠️  WARNING: Basic imports took {basic_imports_time:.3f}s (>0.05s)')
            recommendations.append('Basic imports are slower than expected. Check args.py and log.py for heavy dependencies.')
        return issues + recommendations
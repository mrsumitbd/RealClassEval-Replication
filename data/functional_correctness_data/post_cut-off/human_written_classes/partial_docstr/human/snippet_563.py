from rich.panel import Panel

class EvaluationOutputPanel:
    """Displays evaluation output with truncation for long outputs."""

    def __init__(self):
        self.output = ''

    def update(self, output: str) -> None:
        """Update the evaluation output."""
        self.output = output

    def clear(self) -> None:
        """Clear the evaluation output."""
        self.output = ''

    def get_display(self) -> Panel:
        """Create a panel displaying the evaluation output with truncation if needed."""
        return Panel(self.output, title='[bold]📋 Evaluation Output', border_style='blue', expand=True, padding=(0, 1))
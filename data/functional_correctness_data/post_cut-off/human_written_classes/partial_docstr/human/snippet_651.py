import time
import os

class ReplInterruptHandler:
    """Handles interrupt signals for the REPL with double-press detection."""

    def __init__(self, console):
        self.console = console
        self.last_interrupt_time = 0
        self.interrupt_count = 0
        self.double_press_window = 0.5

    def __call__(self, signum, frame):
        """Handle SIGINT with double-press detection."""
        current_time = time.time()
        time_since_last = current_time - self.last_interrupt_time
        if time_since_last <= self.double_press_window and self.interrupt_count >= 1:
            self.console.print('\n\n[bold red]Double interrupt detected. Exiting Katalyst...[/bold red]')
            self.console.print('[green]Goodbye![/green]')
            os._exit(0)
        else:
            self.interrupt_count = 1
            self.last_interrupt_time = current_time
            self.console.print('\n[yellow]Press Ctrl+C again to exit Katalyst.[/yellow]')
            raise KeyboardInterrupt()
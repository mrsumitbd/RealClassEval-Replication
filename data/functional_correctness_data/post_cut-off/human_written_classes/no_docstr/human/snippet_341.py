from pathlib import Path
from rich.console import Console
from timecopilot.agent import TimeCopilot as TimeCopilotAgent

class TimeCopilot:

    def __init__(self):
        self.console = Console()

    def forecast(self, path: str | Path, llm: str='openai:gpt-4o-mini', freq: str | None=None, h: int | None=None, seasonality: int | None=None, query: str | None=None, retries: int=3):
        with self.console.status('[bold blue]TimeCopilot is navigating through time...[/bold blue]'):
            forecasting_agent = TimeCopilotAgent(llm=llm, retries=retries)
            result = forecasting_agent.forecast(df=path, freq=freq, h=h, seasonality=seasonality, query=query)
        result.output.prettify(self.console, features_df=result.features_df, eval_df=result.eval_df, fcst_df=result.fcst_df)
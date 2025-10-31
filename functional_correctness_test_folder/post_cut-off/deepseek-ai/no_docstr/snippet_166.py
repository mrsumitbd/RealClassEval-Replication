
import argparse


class SearchAssistantConfig:

    def __init__(self, args: argparse.Namespace):
        self.args = args

    def validate(self) -> None:
        if not hasattr(self.args, 'query'):
            raise ValueError("Missing required argument: 'query'")

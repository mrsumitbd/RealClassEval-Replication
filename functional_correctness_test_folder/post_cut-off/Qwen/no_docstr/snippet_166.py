
import argparse


class SearchAssistantConfig:

    def __init__(self, args: argparse.Namespace):
        self.args = args

    def validate(self) -> None:
        if not hasattr(self.args, 'query'):
            raise ValueError("Missing 'query' argument")
        if not isinstance(self.args.query, str):
            raise ValueError("'query' argument must be a string")
        if hasattr(self.args, 'max_results') and not isinstance(self.args.max_results, int):
            raise ValueError("'max_results' argument must be an integer")
        if hasattr(self.args, 'timeout') and not isinstance(self.args.timeout, (int, float)):
            raise ValueError("'timeout' argument must be a number")

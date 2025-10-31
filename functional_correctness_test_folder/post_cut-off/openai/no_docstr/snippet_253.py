
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class PromptLogger:
    """
    A simple logger for storing prompts and their metadata in a JSON-lines file.
    """

    def __init__(self, log_file: str = "log.txt"):
        """
        Initialize the logger.

        Parameters
        ----------
        log_file : str, optional
            Path to the log file. Defaults to "log.txt".
        """
        self.log_file = log_file
        # Ensure the log file exists
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                pass

    def _write_log(self, entry: Dict):
        """
        Internal helper to write a single log entry as a JSON line.
        """
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def log_prompt(
        self,
        messages: List[Dict[str, str]],
        character_name: Optional[str] = None,
        user_query: Optional[str] = None,
    ):
        """
        Log a prompt represented as a list of message dictionaries.

        Parameters
        ----------
        messages : List[Dict[str, str]]
            List of message dicts, each containing at least 'role' and 'content'.
        character_name : str, optional
            Name of the character involved in the prompt.
        user_query : str, optional
            The raw user query that triggered the prompt.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "prompt",
            "character_name": character_name,
            "user_query": user_query,
            "messages": messages,
        }
        self._write_log(entry)

    def log_formatted_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        memory_context: str = "",
        character_name: Optional[str] = None,
        user_query: Optional[str] = None,
    ):
        """
        Log a formatted prompt consisting of system, user, and optional memory context.

        Parameters
        ----------
        system_prompt : str
            The system prompt text.
        user_prompt : str
            The user prompt text.
        memory_context : str, optional
            Any memory context to include.
        character_name : str, optional
            Name of the character involved in the prompt.
        user_query : str, optional
            The raw user query that triggered the prompt.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "formatted_prompt",
            "character_name": character_name,
            "user_query": user_query,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "memory_context": memory_context,
        }
        self._write_log(entry)

    def get_recent_logs(self, count: int = 10) -> List[Dict]:
        """
        Retrieve the most recent log entries.

        Parameters
        ----------
        count : int, optional
            Number of recent entries to return. Defaults to 10.

        Returns
        -------
        List[Dict]
            List of log entry dictionaries, most recent first.
        """
        if not os.path.exists(self.log_file):
            return []

        with open(self.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Parse JSON lines
        entries = [json.loads(line) for line in lines if line.strip()]
        # Return the last `count` entries in reverse chronological order
        return entries[-count:][::-1]

    def clear_logs(self):
        """
        Clear all logs by truncating the log file.
        """
        with open(self.log_file, "w", encoding="utf-8") as f:
            pass

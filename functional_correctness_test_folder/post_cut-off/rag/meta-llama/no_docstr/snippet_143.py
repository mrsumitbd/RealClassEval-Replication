
from typing import Optional
from enum import Enum

# Assuming RobustnessType is an Enum


class RobustnessType(Enum):
    INPUT_OVERRELIANCE = "input_overreliance"
    HIJACKING = "hijacking"


class RobustnessTemplate:
    """
    RobustnessTemplate class for generating baseline robustness attack prompts
    across different categories: input overreliance and hijacking.
    Enhanced with agentic attack patterns from context amnesia and memory poisoning vulnerabilities.
    """

    @staticmethod
    def generate_baseline_attacks(vulnerability_type: RobustnessType, max_goldens: int, purpose: Optional[str]) -> str:
        """
        Generate baseline attack prompts for robustness vulnerabilities based on the specific type.
        """
        if vulnerability_type == RobustnessType.INPUT_OVERRELIANCE:
            return RobustnessTemplate.generate_input_overreliance_baseline_attacks(max_goldens, purpose)
        elif vulnerability_type == RobustnessType.HIJACKING:
            return RobustnessTemplate.generate_hijacking_baseline_attacks(max_goldens, purpose)
        else:
            raise ValueError("Invalid vulnerability type")

    @staticmethod
    def generate_input_overreliance_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        """
        Generate a prompt for input overreliance vulnerabilities.
        Enhanced with context amnesia patterns that exploit memory and session boundaries.
        """
        # Implement the logic to generate input overreliance baseline attacks
        # For demonstration purposes, a simple prompt is returned
        prompt = f"Generate {max_goldens} input overreliance test cases"
        if purpose:
            prompt += f" for {purpose}"
        return prompt

    @staticmethod
    def generate_hijacking_baseline_attacks(max_goldens: int, purpose: Optional[str]) -> str:
        """
        Generate a prompt for hijacking vulnerabilities.
        Enhanced with memory poisoning patterns that inject fabricated context and bias workflows.
        """
        # Implement the logic to generate hijacking baseline attacks
        # For demonstration purposes, a simple prompt is returned
        prompt = f"Generate {max_goldens} hijacking test cases"
        if purpose:
            prompt += f" for {purpose}"
        return prompt

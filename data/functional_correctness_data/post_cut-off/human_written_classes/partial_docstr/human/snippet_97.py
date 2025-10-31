import time
from typing import List, Optional

class AmpResponseProcessor:
    """Handles processing and extraction of Amp responses from terminal output"""

    def __init__(self, wrapper: 'AmpWrapper'):
        self.wrapper = wrapper
        self.response_buffer: List[str] = []
        self.inference_started = False
        self.has_response_content = False
        self.last_activity_time = 0.0

    def reset(self):
        """Reset processor state for new response"""
        self.response_buffer = []
        self.inference_started = False
        self.has_response_content = False
        self.last_activity_time = time.time()

    def add_output_chunk(self, output: str) -> bool:
        """
        Add output chunk and return True if processing started
        Returns True if inference detection triggered
        """
        clean_output = self.wrapper.strip_ansi(output)
        if 'Running inference' in clean_output:
            if not self.inference_started:
                self.wrapper.log('[INFO] AMP started processing')
                self.inference_started = True
                self.reset()
                self.wrapper.message_processor.process_assistant_message_sync('AMP is processing your request...')
                return True
        if self.inference_started:
            self.response_buffer.append(output)
            self.last_activity_time = time.time()
            self.wrapper.log(f'[DEBUG] Buffering chunk ({len(output)} chars)')
            if not self.has_response_content:
                self.has_response_content = self._detect_response_content(clean_output)
        return False

    def _detect_response_content(self, clean_output: str) -> bool:
        """Detect if output contains actual response content (not just thinking)"""
        lines = clean_output.split('\n')
        for line in lines:
            stripped = line.strip()
            if any((ui in line for ui in ['───', '╭', '╮', '╯', '╰', '│', 'Ctrl+R', '┃'])):
                continue
            if stripped and len(stripped) > 5 and (not stripped.startswith('The user')) and ('not a request' not in stripped.lower()) and ('following the guidelines' not in stripped.lower()) and ('I should' not in stripped.lower()) and ("I don't need" not in stripped.lower()) and ('need to use' not in stripped.lower()) and ('Thinking' not in stripped) and ('Running inference' not in stripped):
                if stripped[0].isupper() and ('!' in stripped or '?' in stripped or '.' in stripped):
                    self.wrapper.log(f'[INFO] Detected actual response: {stripped[:50]}')
                    return True
        return False

    def check_completion(self, clean_output: str) -> bool:
        """Check if response is complete based on output markers"""
        if 'Thread:' in clean_output or 'Continue this thread' in clean_output:
            return True
        return False

    def is_idle_complete(self) -> bool:
        """Check if response is complete due to idle timeout"""
        if self.inference_started and self.has_response_content and (time.time() - self.last_activity_time > 2.0):
            return True
        return False

    def extract_response(self) -> str:
        """Extract the final response from buffered output - SIMPLIFIED VERSION"""
        if not self.response_buffer:
            return 'AMP has completed processing.'
        full_output = ''.join(self.response_buffer)
        self.wrapper.log(f'[DEBUG] Extracting from {len(full_output)} chars')
        response_lines = []
        seen_lines = set()
        for line in full_output.split('\n'):
            clean_line = self.wrapper.strip_ansi(line).strip()
            if not clean_line or any((ui in clean_line for ui in ['───', '╭', '╮', '╯', '╰', '│', 'Running inference', 'Ctrl+R', 'Thread:', 'Continue this thread', '┃'])):
                continue
            if any((thinking in clean_line.lower() for thinking in ['thinking', 'i need to', 'i should', 'the user', 'according to', 'this is a', 'this seems', 'let me analyze'])):
                continue
            if len(clean_line) > 10 and clean_line not in seen_lines:
                response_lines.append(clean_line)
                seen_lines.add(clean_line)
        if response_lines:
            response_text = '\n'.join(response_lines)
            self.wrapper.log(f'[INFO] Extracted response ({len(response_text)} chars)')
            return response_text
        else:
            return 'AMP has completed processing.'
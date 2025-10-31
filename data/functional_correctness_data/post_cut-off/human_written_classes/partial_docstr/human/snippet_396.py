from src.exceptions import DeviceConfigError, TCLBuilderError, TemplateNotFoundError, XDCConstraintError
from src.string_utils import generate_tcl_header_comment, get_project_name, log_debug_safe, log_error_safe, log_info_safe, log_warning_safe, safe_format
import shutil
from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable
import logging
from pathlib import Path

class ConstraintManager:
    """Manages XDC constraint file operations."""

    def __init__(self, output_dir: Path, logger: logging.Logger):
        self.output_dir = output_dir
        self.logger = logger

    def copy_xdc_files(self, board_name: str) -> List[str]:
        """
        Copy XDC files from repository to output directory.

        Args:
            board_name: Name of the board to get XDC files for

        Returns:
            List of copied file names

        Raises:
            XDCConstraintError: If XDC files cannot be found or copied
        """
        try:
            from file_management.repo_manager import get_xdc_files, is_repository_accessible
            if not is_repository_accessible(board_name):
                raise XDCConstraintError('Repository is not accessible')
            xdc_files = get_xdc_files(board_name)
            if not xdc_files:
                raise XDCConstraintError(safe_format("No XDC files found for board '{board}'", board=board_name))
            copied_files = []
            for xdc_file in xdc_files:
                dest_path = self.output_dir / xdc_file.name
                try:
                    shutil.copy2(xdc_file, dest_path)
                    copied_files.append(dest_path.name)
                    log_info_safe(self.logger, safe_format('Copied XDC file: {filename}', filename=xdc_file.name))
                except Exception as e:
                    raise XDCConstraintError(safe_format('Failed to copy XDC file {filename}: {error}', filename=xdc_file.name, error=e)) from e
            log_info_safe(self.logger, safe_format('Successfully copied {count} XDC files', count=len(copied_files)))
            return copied_files
        except Exception as e:
            if isinstance(e, XDCConstraintError):
                raise
            raise XDCConstraintError(safe_format("Failed to copy XDC files for board '{board}': {error}", board=board_name, error=e)) from e
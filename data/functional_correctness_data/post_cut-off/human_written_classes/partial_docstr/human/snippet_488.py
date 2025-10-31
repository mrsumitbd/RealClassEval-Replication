import os
import shutil
import tempfile

class TemporaryFile:
    """
    Manages a temporary file
    """

    def __init__(self, initial_content: str=''):
        """
        Initializes the TemporaryFile by creating a physical temporary file with initial_content.
        """
        self.path: str = self._create_new_file_with_content(initial_content)

    def _create_new_file_with_content(self, content: str) -> str:
        """
        Core logic to create a new temporary file, write content, and return its path.
        The created file handle is closed after writing.
        """
        tf = None
        try:
            tf = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.jrdev_tmp')
            tf.write(content)
            created_path = tf.name
            return created_path
        except Exception as e:
            if tf and tf.name and os.path.exists(tf.name):
                try:
                    os.unlink(tf.name)
                except OSError as unlink_err:
                    logger.error(f'Failed to unlink partially created temp file {tf.name} after error: {unlink_err}')
            logger.error(f'Failed to create temporary file: {e}', exc_info=True)
            raise TempFileCreationError(f'Failed to create temporary file: {e}') from e
        finally:
            if tf:
                tf.close()

    def overwrite(self, new_content: str) -> None:
        """
        Replaces the current temporary file with a new one containing new_content.
        The old temporary file is unlinked.
        """
        old_path = self.path
        new_temp_path = None
        try:
            new_temp_path = self._create_new_file_with_content(new_content)
            self.path = new_temp_path
            if old_path and os.path.exists(old_path):
                try:
                    os.unlink(old_path)
                except OSError as e:
                    logger.warning(f'Could not unlink old temp file {old_path} during overwrite: {e}')
        except TempFileCreationError:
            self.path = old_path
            raise
        except Exception as e:
            self.path = old_path
            logger.error(f'Unexpected error during overwrite. Old path: {old_path}, New content attempted. Error: {e}', exc_info=True)
            raise TempFileOperationError(f'Unexpected error during overwrite: {e}') from e

    def save_to(self, destination_path: str) -> None:
        """
        Creates destination directories if they don't exist.
        """
        if not self.path or not os.path.exists(self.path):
            msg = f"Temporary file path '{self.path}' is invalid or file does not exist. Cannot save."
            logger.error(msg)
            raise TempFileAccessError(msg)
        try:
            directory = os.path.dirname(destination_path)
            if directory and (not os.path.exists(directory)):
                os.makedirs(directory)
            shutil.copy2(self.path, destination_path)
            logger.info(f'Temporary file {self.path} successfully saved to {destination_path}')
        except Exception as e:
            logger.error(f'Error saving temp file {self.path} to {destination_path}: {e}', exc_info=True)
            raise TempFileOperationError(f'Failed to save temporary file to {destination_path}: {e}') from e

    def get_current_path(self) -> str:
        """Returns the path of the current temporary file."""
        if not self.path:
            msg = 'Temporary file path is not set (TemporaryFile.path is None).'
            logger.error(msg)
            raise TempFileAccessError(msg)
        return self.path

    def cleanup(self) -> None:
        """
        Deletes the current temporary file from the filesystem.
        """
        if self.path and os.path.exists(self.path):
            try:
                os.unlink(self.path)
                logger.debug(f'Cleaned up temp file: {self.path}')
            except OSError as e:
                logger.error(f'Error unlinking temp file {self.path} during cleanup: {e}')
        self.path = None

    def __enter__(self):
        if not self.path:
            raise TempFileAccessError('TemporaryFile entered but path is not initialized. __init__ might have failed.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
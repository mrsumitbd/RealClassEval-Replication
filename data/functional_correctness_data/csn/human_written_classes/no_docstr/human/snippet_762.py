class FileEndingUtil:
    WINDOWS_LINE_ENDING = b'\r\n'
    LINUX_LINE_ENDING = b'\n'

    @staticmethod
    def windows2linux(content: bytes) -> bytes:
        assert isinstance(content, bytes)
        return content.replace(FileEndingUtil.WINDOWS_LINE_ENDING, FileEndingUtil.LINUX_LINE_ENDING)

    @staticmethod
    def linux2windows(content: bytes) -> bytes:
        return content.replace(FileEndingUtil.LINUX_LINE_ENDING, FileEndingUtil.WINDOWS_LINE_ENDING)

    @staticmethod
    def convert_to_linux_style_file(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
            content = FileEndingUtil.windows2linux(content)
        with open(file_path, 'wb') as f:
            f.write(content)

    @staticmethod
    def convert_to_windows_style_file(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
            content = FileEndingUtil.linux2windows(content)
        with open(file_path, 'wb') as f:
            f.write(content)
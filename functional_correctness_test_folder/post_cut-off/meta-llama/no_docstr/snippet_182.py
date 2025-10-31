
class OutputSink:
    """
    A base class for output sinks.

    Output sinks are responsible for handling the output of a process or operation.
    They can write the output to various destinations such as files, consoles, or networks.
    """

    def write(self, text: str) -> None:
        """
        Writes the given text to the output sink.

        Args:
        text (str): The text to be written to the output sink.
        """
        raise NotImplementedError("Subclasses must implement the write method")

    def finalize(self) -> None:
        """
        Finalizes the output sink.

        This method is called after all output has been written to the sink.
        It can be used to perform any necessary cleanup or flushing operations.
        """
        pass


class ConsoleOutputSink(OutputSink):
    """
    An output sink that writes to the console.
    """

    def write(self, text: str) -> None:
        print(text, end='')

    def finalize(self) -> None:
        pass


class FileOutputSink(OutputSink):
    """
    An output sink that writes to a file.
    """

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.file = open(filename, 'w')

    def write(self, text: str) -> None:
        self.file.write(text)

    def finalize(self) -> None:
        self.file.close()


# Example usage:
if __name__ == "__main__":
    console_sink = ConsoleOutputSink()
    file_sink = FileOutputSink('output.txt')

    sinks = [console_sink, file_sink]

    for sink in sinks:
        sink.write("Hello, ")
        sink.write("World!")
        sink.finalize()

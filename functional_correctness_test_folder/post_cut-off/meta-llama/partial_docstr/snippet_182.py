
class OutputSink:
    '''Abstract output sink for processed markdown text.'''

    def write(self, text: str) -> None:
        raise NotImplementedError("Subclasses must implement the write method")

    def finalize(self) -> None:
        raise NotImplementedError(
            "Subclasses must implement the finalize method")


class FileOutputSink(OutputSink):
    '''Output sink that writes to a file.'''

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.file = open(filename, 'w')

    def write(self, text: str) -> None:
        self.file.write(text)

    def finalize(self) -> None:
        self.file.close()


class ConsoleOutputSink(OutputSink):
    '''Output sink that writes to the console.'''

    def write(self, text: str) -> None:
        print(text, end='')

    def finalize(self) -> None:
        pass


class StringOutputSink(OutputSink):
    '''Output sink that accumulates output in a string.'''

    def __init__(self) -> None:
        self.output = ''

    def write(self, text: str) -> None:
        self.output += text

    def finalize(self) -> None:
        pass

    def get_output(self) -> str:
        return self.output


# Example usage:
if __name__ == "__main__":
    file_sink = FileOutputSink('output.txt')
    file_sink.write('Hello, ')
    file_sink.write('world!')
    file_sink.finalize()

    console_sink = ConsoleOutputSink()
    console_sink.write('Hello, ')
    console_sink.write('world!')
    console_sink.finalize()

    string_sink = StringOutputSink()
    string_sink.write('Hello, ')
    string_sink.write('world!')
    string_sink.finalize()
    print(string_sink.get_output())


from abc import ABC, abstractmethod


class OutputSink(ABC):
    '''Abstract output sink for processed markdown text.'''

    @abstractmethod
    def write(self, text: str) -> None:
        '''Write text to the sink.'''
        pass

    @abstractmethod
    def finalize(self) -> None:
        '''Finalize the output.'''
        pass


class FileOutputSink(OutputSink):
    '''Concrete output sink that writes to a file.'''

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.file = None

    def write(self, text: str) -> None:
        if self.file is None:
            self.file = open(self.filename, 'w')
        self.file.write(text)

    def finalize(self) -> None:
        if self.file is not None:
            self.file.close()


class ConsoleOutputSink(OutputSink):
    '''Concrete output sink that writes to the console.'''

    def write(self, text: str) -> None:
        print(text, end='')

    def finalize(self) -> None:
        pass


class StringOutputSink(OutputSink):
    '''Concrete output sink that accumulates output in a string.'''

    def __init__(self) -> None:
        self.text = ''

    def write(self, text: str) -> None:
        self.text += text

    def finalize(self) -> None:
        pass

    def get_output(self) -> str:
        return self.text


# Example usage:
def main() -> None:
    file_sink = FileOutputSink('output.txt')
    console_sink = ConsoleOutputSink()
    string_sink = StringOutputSink()

    sinks = [file_sink, console_sink, string_sink]

    for sink in sinks:
        sink.write('Hello, ')
        sink.write('world!')
        sink.finalize()

    print('\nOutput from StringOutputSink:')
    print(string_sink.get_output())


if __name__ == '__main__':
    main()

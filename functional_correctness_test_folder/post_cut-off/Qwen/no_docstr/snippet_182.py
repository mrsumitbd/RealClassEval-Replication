
class OutputSink:

    def write(self, text: str) -> None:
        print(text)

    def finalize(self) -> None:
        print("Finalizing output.")

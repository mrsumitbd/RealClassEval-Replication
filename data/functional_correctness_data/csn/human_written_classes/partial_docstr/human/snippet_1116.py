class CanvasObjects:
    """Canvas object collector to store list of canvas objects."""

    def __init__(self):
        self.objects = []

    def __iter__(self) -> iter:
        return iter(self.objects)

    def add(self, canvas_object) -> None:
        self.objects.append(canvas_object)
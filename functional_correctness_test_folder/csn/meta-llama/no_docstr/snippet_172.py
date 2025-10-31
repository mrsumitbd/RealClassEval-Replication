
class MultipleThings:

    def __init__(self, things, name):
        """
        Initialize the MultipleThings class.

        Args:
            things (list): A list of things.
            name (str): The name associated with the things.
        """
        self.things = things
        self.name = name

    def get_thing(self, idx):
        """
        Get a specific thing by its index.

        Args:
            idx (int): The index of the thing to retrieve.

        Returns:
            The thing at the specified index if it exists, otherwise None.
        """
        if idx < len(self.things):
            return self.things[idx]
        else:
            return None

    def get_things(self):
        """
        Get all the things.

        Returns:
            list: A list of all the things.
        """
        return self.things

    def get_name(self):
        """
        Get the name associated with the things.

        Returns:
            str: The name associated with the things.
        """
        return self.name


# Example usage:
def main():
    things = [1, 2, 3, 4, 5]
    name = "Numbers"
    multiple_things = MultipleThings(things, name)

    print(multiple_things.get_name())  # Output: Numbers
    print(multiple_things.get_things())  # Output: [1, 2, 3, 4, 5]
    print(multiple_things.get_thing(2))  # Output: 3
    print(multiple_things.get_thing(10))  # Output: None


if __name__ == "__main__":
    main()

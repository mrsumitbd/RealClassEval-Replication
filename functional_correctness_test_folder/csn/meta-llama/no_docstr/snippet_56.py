
class Collection:
    def __init__(self):
        self.items = []

    def __len__(self) -> int:
        return len(self.items)

    def __delitem__(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            raise KeyError(f"{item} not found in collection")

    def __contains__(self, item) -> bool:
        return item in self.items

    def add(self, item):
        self.items.append(item)

# Example usage:


def main():
    collection = Collection()
    collection.add(1)
    collection.add(2)
    collection.add(3)

    print(len(collection))  # Output: 3
    print(2 in collection)  # Output: True
    del collection[2]
    print(2 in collection)  # Output: False
    try:
        del collection[4]
    except KeyError as e:
        print(e)  # Output: 4 not found in collection


if __name__ == "__main__":
    main()

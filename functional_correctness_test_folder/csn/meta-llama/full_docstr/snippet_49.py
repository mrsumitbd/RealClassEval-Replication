
from abc import ABC, abstractmethod


class QuilAtom(ABC):
    '''Abstract class for atomic elements of Quil.'''

    @abstractmethod
    def out(self) -> str:
        '''Return the element as a valid Quil string.'''
        pass

    @abstractmethod
    def __str__(self) -> str:
        '''Get a string representation of the element, possibly not valid Quil.'''
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        '''Return True if the other object is equal to this one.'''
        pass

    @abstractmethod
    def __hash__(self) -> int:
        '''Return a hash of the object.'''
        pass


# Example implementation of a concrete QuilAtom subclass
class QuilGate(QuilAtom):
    def __init__(self, name: str, params: list[float], qubits: list[int]):
        self.name = name
        self.params = tuple(params)
        self.qubits = tuple(qubits)

    def out(self) -> str:
        param_str = '({})'.format(
            ', '.join(map(str, self.params))) if self.params else ''
        qubit_str = ' '.join(map(str, self.qubits))
        return '{}{} {}'.format(self.name, param_str, qubit_str)

    def __str__(self) -> str:
        return self.out()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuilGate):
            return False
        return (self.name, self.params, self.qubits) == (other.name, other.params, other.qubits)

    def __hash__(self) -> int:
        return hash((self.name, self.params, self.qubits))


# Example usage
if __name__ == "__main__":
    gate = QuilGate('RX', [3.14], [0])
    print(gate.out())  # Output: RX(3.14) 0
    print(str(gate))   # Output: RX(3.14) 0
    gate2 = QuilGate('RX', [3.14], [0])
    print(gate == gate2)  # Output: True
    print(hash(gate) == hash(gate2))  # Output: True

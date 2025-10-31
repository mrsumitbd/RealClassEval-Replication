from dataclasses import dataclass

@dataclass
class BindableRecord:
    bindable: 'Bindable'
    key: str

    def __eq__(self, other: 'BindableRecord'):
        return self.bindable is other.bindable and self.key == other.key

    def __hash__(self):
        return hash((id(self.bindable), self.key))
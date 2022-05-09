


from sys import implementation
from typing import Optional, Set, List
from dataclasses import dataclass
from copy import copy


@dataclass
class Capability:

    implementation: object
    abilities: Set[str]
    name: Optional[str] = None


class KvStore:

    def __init__(self, storage_layers: List[Capability]):
        self.storage_layers = copy(storage_layers)
        self.storage_layers.reverse()  # We priortize calling functions on capabilities at the start of the list
        self.attribute_to_implementation = {}

        for layer in storage_layers:
            for ability in layer.abilities:
                self.attribute_to_implementation[ability] = layer.implementation

    def __getattr__(self, name: str):

        if name not in self.attribute_to_implementation:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attrubute '{name}'. Implementations: {','.join([x.name for x in self.storage_layers])}")

        return getattr(self.attribute_to_implementation[name], name)

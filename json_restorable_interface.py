from abc import ABC, abstractmethod


class JsonRestorable(ABC):

    @abstractmethod
    def to_json(self):
        """Converts the object to JSON format."""
        raise NotImplementedError("The to_json method must be implemented in subclasses.")


    @abstractmethod
    def from_json(self, **kwargs):
        """Change an object from JSON data."""
        raise NotImplementedError("The from_json method must be implemented in subclasses.")


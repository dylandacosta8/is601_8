from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @abstractmethod
    def show_help(self):
        pass
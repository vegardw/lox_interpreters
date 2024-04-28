from typing import Any, List
from abc import ABC, abstractmethod

class Interpreter:
    pass

class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter: Interpreter, arguments: List[Any]):
        pass
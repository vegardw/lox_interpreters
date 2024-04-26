from typing import Any
from .token import Token
from .lox_runtime_error import LoxRuntimeError

class Environment:
    pass

class Environment:

    def __init__(self, enclosing: Environment=None) -> None:
        self.values = {}
        self.enclosing = enclosing

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        if self.enclosing != None:
            self.enclosing.assign(name, value)
            return
        
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        
        if self.enclosing != None:
            return self.enclosing.get(name)
        
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
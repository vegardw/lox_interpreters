from typing import Any, List
from .lox_callable import LoxCallable, Interpreter
from .stmt import FunctionStmt
from .return_obj import Return
from .environment import Environment

class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt, closure: Environment) -> None:
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter: Interpreter, arguments: List[Any]) -> Any:
        environment = Environment(self.closure)

        for i, _ in enumerate(self.declaration.params):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as r:
            return r.value

    def arity(self) -> int:
        return len(self.declaration.params)
    
    def __str__(self) -> str:
        return f'<fn {self.declaration.name.lexeme}>'
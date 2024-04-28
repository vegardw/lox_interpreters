from abc import ABC, abstractmethod
from typing import Any, List
from .token import Token
from .expr import Expr


# Forward declarations, needed for declaring visitor interface before the actual classes
class BlockStmt:
  pass
class ExpressionStmt:
  pass
class IfStmt:
  pass
class PrintStmt:
  pass
class VarStmt:
  pass
class WhileStmt:
  pass


# StmtVisitor interface
class StmtVisitor(ABC):
  @abstractmethod
  def visit_block_stmt(self, stmt: BlockStmt):
    pass
  @abstractmethod
  def visit_expression_stmt(self, stmt: ExpressionStmt):
    pass
  @abstractmethod
  def visit_if_stmt(self, stmt: IfStmt):
    pass
  @abstractmethod
  def visit_print_stmt(self, stmt: PrintStmt):
    pass
  @abstractmethod
  def visit_var_stmt(self, stmt: VarStmt):
    pass
  @abstractmethod
  def visit_while_stmt(self, stmt: WhileStmt):
    pass


# Stmt base class and sub classes
class Stmt(ABC):
  @abstractmethod
  def accept(self, visitor: StmtVisitor):
    pass

class BlockStmt(Stmt):
  def __init__(self, statements: List[Stmt]) -> None:
    self.statements = statements

  def accept(self, visitor: StmtVisitor):
    return visitor.visit_block_stmt(self)

class ExpressionStmt(Stmt):
  def __init__(self, expression: Expr) -> None:
    self.expression = expression

  def accept(self, visitor: StmtVisitor):
    return visitor.visit_expression_stmt(self)

class IfStmt(Stmt):
  def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt) -> None:
    self.condition = condition
    self.thenBranch = thenBranch
    self.elseBranch = elseBranch

  def accept(self, visitor: StmtVisitor):
    return visitor.visit_if_stmt(self)

class PrintStmt(Stmt):
  def __init__(self, expression: Expr) -> None:
    self.expression = expression

  def accept(self, visitor: StmtVisitor):
    return visitor.visit_print_stmt(self)

class VarStmt(Stmt):
  def __init__(self, name: Token, initializer: Expr) -> None:
    self.name = name
    self.initializer = initializer

  def accept(self, visitor: StmtVisitor):
    return visitor.visit_var_stmt(self)

class WhileStmt(Stmt):
  def __init__(self, condition: Expr, body: Stmt) -> None:
    self.condition = condition
    self.body = body

  def accept(self, visitor: StmtVisitor):
    return visitor.visit_while_stmt(self)

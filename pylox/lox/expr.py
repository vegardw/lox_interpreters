from abc import ABC, abstractmethod
from typing import Any, List
from .token import Token


# Forward declarations, needed for declaring visitor interface before the actual classes
class AssignExpr:
  pass
class BinaryExpr:
  pass
class CallExpr:
  pass
class GroupingExpr:
  pass
class LiteralExpr:
  pass
class LogicalExpr:
  pass
class UnaryExpr:
  pass
class VariableExpr:
  pass


# ExprVisitor interface
class ExprVisitor(ABC):
  @abstractmethod
  def visit_assign_expr(self, expr: AssignExpr):
    pass
  @abstractmethod
  def visit_binary_expr(self, expr: BinaryExpr):
    pass
  @abstractmethod
  def visit_call_expr(self, expr: CallExpr):
    pass
  @abstractmethod
  def visit_grouping_expr(self, expr: GroupingExpr):
    pass
  @abstractmethod
  def visit_literal_expr(self, expr: LiteralExpr):
    pass
  @abstractmethod
  def visit_logical_expr(self, expr: LogicalExpr):
    pass
  @abstractmethod
  def visit_unary_expr(self, expr: UnaryExpr):
    pass
  @abstractmethod
  def visit_variable_expr(self, expr: VariableExpr):
    pass


# Expr base class and sub classes
class Expr(ABC):
  @abstractmethod
  def accept(self, visitor: ExprVisitor):
    pass

class AssignExpr(Expr):
  def __init__(self, name: Token, value: Expr) -> None:
    self.name = name
    self.value = value

  def accept(self, visitor: ExprVisitor):
    return visitor.visit_assign_expr(self)

class BinaryExpr(Expr):
  def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
    self.left = left
    self.operator = operator
    self.right = right

  def accept(self, visitor: ExprVisitor):
    return visitor.visit_binary_expr(self)

class CallExpr(Expr):
  def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]) -> None:
    self.callee = callee
    self.paren = paren
    self.arguments = arguments

  def accept(self, visitor: ExprVisitor):
    return visitor.visit_call_expr(self)

class GroupingExpr(Expr):
  def __init__(self, expression: Expr) -> None:
    self.expression = expression

  def accept(self, visitor: ExprVisitor):
    return visitor.visit_grouping_expr(self)

class LiteralExpr(Expr):
  def __init__(self, value: Any) -> None:
    self.value = value

  def accept(self, visitor: ExprVisitor):
    return visitor.visit_literal_expr(self)

class LogicalExpr(Expr):
  def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
    self.left = left
    self.operator = operator
    self.right = right

  def accept(self, visitor: ExprVisitor):
    return visitor.visit_logical_expr(self)

class UnaryExpr(Expr):
  def __init__(self, operator: Token, right: Expr) -> None:
    self.operator = operator
    self.right = right

  def accept(self, visitor: ExprVisitor):
    return visitor.visit_unary_expr(self)

class VariableExpr(Expr):
  def __init__(self, name: Token) -> None:
    self.name = name

  def accept(self, visitor: ExprVisitor):
    return visitor.visit_variable_expr(self)

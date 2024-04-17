from abc import ABC, abstractmethod
from typing import Any
from .token import Token

class BinaryExpr:
  pass
class GroupingExpr:
  pass
class LiteralExpr:
  pass
class UnaryExpr:
  pass

class ExprVisitor(ABC):
  @abstractmethod
  def visit_binary_expr(self, expr: BinaryExpr) -> str:
    pass

  @abstractmethod
  def visit_grouping_expr(self, expr: GroupingExpr) -> str:
    pass

  @abstractmethod
  def visit_literal_expr(self, expr: LiteralExpr) -> str:
    pass

  @abstractmethod
  def visit_unary_expr(self, expr: UnaryExpr) -> str:
    pass

class Expr(ABC):
  @abstractmethod
  def accept(self, visitor: ExprVisitor):
    pass

class BinaryExpr(Expr):
  def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
    self.left = left
    self.operator = operator
    self.right = right
    
  def accept(self, visitor: ExprVisitor):
    return visitor.visit_binary_expr(self)
  
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
  
class UnaryExpr(Expr):
  def __init__(self, operator: Token, right: Expr) -> None:
    self.operator = operator
    self.right = right

  def accept(self, visitor: ExprVisitor):
    return visitor.visit_unary_expr(self)
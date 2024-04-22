from .expr import *
from .token import *
from .lox_runtime_error import LoxRuntimeError
from .lox import runtime_error
from typing import Any

class Interpreter(ExprVisitor):

  def interpret(self, expression: Expr):
    try:
      value = self.evaluate(expression)
      print(self.stringify(value))
    except LoxRuntimeError as e:
      runtime_error(e)

  def visit_literal_expr(self, expr: LiteralExpr) -> Any:
    return expr.value
  
  def visit_grouping_expr(self, expr: GroupingExpr) -> Any:
    return self.evaluate(expr.expression)
  
  def visit_unary_expr(self, expr: UnaryExpr) -> Any:
    right = self.evaluate(expr.right)

    if expr.operator.type == TokenType.MINUS:
      self.check_number_operand(expr.operator, right)
      return -float(right)
    elif expr.operator.type == TokenType.BANG:
      return not self.is_truthy(right)
    
    return None
  
  def visit_binary_expr(self, expr: BinaryExpr):
    left = self.evaluate(expr.left)
    right = self.evaluate(expr.right)

    if expr.operator.type == TokenType.MINUS:
      self.check_number_operands(expr.operator, left, right)
      return float(left) - float(right)
    elif expr.operator.type == TokenType.SLASH:
      self.check_number_operands(expr.operator, left, right)
      return float(left) / float(right)
    elif expr.operator.type == TokenType.STAR:
      self.check_number_operands(expr.operator, left, right)
      return float(left) * float(right)
    elif expr.operator.type == TokenType.PLUS:
      if isinstance(left, float) and isinstance(right, float):
        return float(left) + float(right)
      if isinstance(left, str) and isinstance(right, str):
        return str(left) + str(right)
      raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
    elif expr.operator.type == TokenType.GREATER:
      self.check_number_operands(expr.operator, left, right)
      return float(left) > float(right)
    elif expr.operator.type == TokenType.GREATER_EQUAL:
      self.check_number_operands(expr.operator, left, right)
      return float(left) >= float(right)
    elif expr.operator.type == TokenType.LESS:
      self.check_number_operands(expr.operator, left, right)
      return float(left) < float(right)
    elif expr.operator.type == TokenType.LESS_EQUAL:
      self.check_number_operands(expr.operator, left, right)
      return float(left) <= float(right)
    elif expr.operator.type == TokenType.BANG_EQUAL:
      return not self.is_equal(left, right)
    elif expr.operator.type == TokenType.EQUAL_EQUAL:
      return self.is_equal(left, right)
    
    # Unreachable
    return None
  
  def stringify(self, object: Any) -> str:
    if object is None: return 'nil'
    if object == True: return 'true'
    if object == False: return 'false'

    if isinstance(object, float):
      text = str(object)
      if text[-2:] == '.0':
        text = text[:-2]
      return text
    
    return str(object)

  def check_number_operand(self, operator: Token, operand: Any) -> None:
    if isinstance(operator, float): return
    raise LoxRuntimeError(operator, "Operand must be a number.")
  
  def check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
    if isinstance(left, float) and isinstance(right, float): return
    raise LoxRuntimeError(operator, "Operands must be numbers.")

  def is_equal(self, a: Any, b: Any) -> bool:
    if a is None and b is None: return True
    if a is None: return False
    return a == b

  def is_truthy(self, object: Any) -> bool:
    if object is None: return False
    if isinstance(object, bool): return bool(object)
    return True

  def evaluate(self, expr: Expr) -> Any:
    return expr.accept(self)
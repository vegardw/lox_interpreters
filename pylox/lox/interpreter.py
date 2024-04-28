from lox.lox_callable import Interpreter
from .expr import *
from .stmt import *
from .token import *
from .lox_callable import *
from .lox_function import LoxFunction
from .lox_runtime_error import LoxRuntimeError
from .lox import runtime_error
from .environment import Environment
from .return_obj import Return
from typing import Any, List
from time import time

class Interpreter(ExprVisitor, StmtVisitor):

  def __init__(self) -> None:
    self.globals = Environment()
    self.environment = self.globals

    class ClockNativeFn(LoxCallable):
      def arity(self) -> int:
        return 0
      
      def call(self, interpreter: Interpreter, arguments: List[Any]):
        return float(time())
      
      def __str__(self) -> str:
        return "<native fn>"
    
    self.globals.define("clock", ClockNativeFn())

  def interpret(self, statements: List[Stmt]):
    try:
      for statement in statements:
        self.execute(statement)
    except LoxRuntimeError as e:
      runtime_error(e)

  def visit_literal_expr(self, expr: LiteralExpr) -> Any:
    return expr.value
  
  def visit_logical_expr(self, expr: LogicalExpr) -> Any:
    left = self.evaluate(expr.left)

    if expr.operator.type == TokenType.OR:
      if self.is_truthy(left): return left
    else:
      if not self.is_truthy(left): return left

    return self.evaluate(expr.right)

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
  
  def visit_variable_expr(self, expr: VariableExpr) -> Any:
    return self.environment.get(expr.name)

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
  
  def visit_call_expr(self, expr: CallExpr) -> Any:
    callee = self.evaluate(expr.callee)

    arguments = []
    for argument in expr.arguments:
      arguments.append(self.evaluate(argument))

    if not isinstance(callee, LoxCallable):
      raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

    fn: LoxCallable = callee
    if len(arguments) != fn.arity():
      raise LoxRuntimeError(expr.paren, f'Expected {fn.arity()} arguments but got {len(arguments)}.')
    return fn.call(self, arguments)
  
  def stringify(self, object: Any) -> str:
    if isinstance(object, float):
      text = str(object)
      if text[-2:] == '.0':
        text = text[:-2]
      return text
    
    if object == None: return 'nil'
    if object == True: return 'true'
    if object == False: return 'false'
    
    return str(object)

  def check_number_operand(self, operator: Token, operand: Any) -> None:
    if isinstance(operator, float): return
    raise LoxRuntimeError(operator, "Operand must be a number.")
  
  def check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
    if isinstance(left, float) and isinstance(right, float): return
    raise LoxRuntimeError(operator, "Operands must be numbers.")

  def is_equal(self, a: Any, b: Any) -> bool:
    if a == None and b == None: return True
    if a == None: return False
    return a == b

  def is_truthy(self, object: Any) -> bool:
    if object == None: return False
    if isinstance(object, bool): return bool(object)
    return True

  def evaluate(self, expr: Expr) -> Any:
    return expr.accept(self)
  
  def execute(self, stmt: Stmt) -> None:
    stmt.accept(self)

  def execute_block(self, statements: List[Stmt], environment: Environment) -> None:
    previous = self.environment
    try:
      self.environment = environment

      for statement in statements:
        self.execute(statement)
    finally:
      self.environment = previous

  def visit_block_stmt(self, stmt: BlockStmt) -> None:
    self.execute_block(stmt.statements, Environment(self.environment))
  
  def visit_expression_stmt(self, stmt: ExpressionStmt) -> None:
    self.evaluate(stmt.expression)

  def visit_function_stmt(self, stmt: FunctionStmt) -> None:
    fn = LoxFunction(stmt, self.environment)
    self.environment.define(stmt.name.lexeme, fn)

  def visit_if_stmt(self, stmt: IfStmt) -> None:
    if self.is_truthy(self.evaluate(stmt.condition)):
      self.execute(stmt.thenBranch)
    elif stmt.elseBranch != None:
      self.execute(stmt.elseBranch)

  def visit_print_stmt(self, stmt: PrintStmt) -> None:
    value = self.evaluate(stmt.expression)
    print(self.stringify(value))

  def visit_return_stmt(self, stmt: ReturnStmt) -> None:
    value = None
    if stmt.value != None: value = self.evaluate(stmt.value)

    raise Return(value)

  def visit_var_stmt(self, stmt: VarStmt) -> None:
    value = None
    if stmt.initializer != None:
      value = self.evaluate(stmt.initializer)

    self.environment.define(stmt.name.lexeme, value)

  def visit_while_stmt(self, stmt: WhileStmt) -> None:
    while self.is_truthy(self.evaluate(stmt.condition)):
      self.execute(stmt.body)

  def visit_assign_expr(self, expr: AssignExpr) -> Any:
    value = self.evaluate(expr.value)
    self.environment.assign(expr.name, value)
    return value
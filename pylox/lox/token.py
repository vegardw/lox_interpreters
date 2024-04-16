from enum import Enum
from typing import Any

TokenType = Enum('TokenType', [
  # Single-character tokens.
  'LEFT_PAREN', 'RIGHT_PAREN', 'LEFT_BRACE', 'RIGHT_BRACE',
  'COMMA', 'DOT', 'MINUS', 'PLUS', 'SEMICOLON', 'SLASH', 'STAR',

  # One or two character tokens.
  'BANG', 'BANG_EQUAL',
  'EQUAL', 'EQUAL_EQUAL',
  'GREATER', 'GREATER_EQUAL',
  'LESS', 'LESS_EQUAL',

  # Literals.
  'IDENTIFIER', 'STRING', 'NUMBER',

  # Keywords.
  'AND', 'CLASS', 'ELSE', 'FALSE', 'FUN', 'FOR', 'IF', 'NIL', 'OR',
  'PRINT', 'RETURN', 'SUPER', 'THIS', 'TRUE', 'VAR', 'WHILE',

  'EOF'
])

class Token:
  def __init__(self, type: TokenType, lexeme: str, literal: Any, line: int) -> None:
    self.type = type
    self.lexeme = lexeme
    self.literal = literal
    self.line = line

  def __str__(self) -> str:
    return f'{self.type} {self.lexeme} {self.literal}'
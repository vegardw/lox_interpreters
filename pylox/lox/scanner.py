from .token import Token, TokenType
from .lox import scanner_error
from typing import List, Any

keywords = {
  'and'    : TokenType.AND,
  'class'  : TokenType.CLASS,
  'else'   : TokenType.ELSE,
  'false'  : TokenType.FALSE,
  'for'    : TokenType.FOR,
  'fun'    : TokenType.FUN,
  'if'     : TokenType.IF,
  'nil'    : TokenType.NIL,
  'or'     : TokenType.OR,
  'print'  : TokenType.PRINT,
  'return' : TokenType.RETURN,
  'super'  : TokenType.SUPER,
  'this'   : TokenType.THIS,
  'true'   : TokenType.TRUE,
  'var'    : TokenType.VAR,
  'while'  : TokenType.WHILE
}

class Scanner:
  
  def __init__(self, source: str) -> None:
    self.source = source
    self.tokens = []
    self.start = 0
    self.current = 0
    self.line = 1

  def scan_tokens(self) -> List[Token]:
    while not self.is_at_end():
      # We are at the beginning of the next lexeme.
      self.start = self.current
      self.scan_token()

    self.tokens.append(Token(TokenType.EOF, '', None, self.line))
    return self.tokens
  
  def scan_token(self) -> None:
    c = self.advance()

    if   c == '(': self.add_null_token(TokenType.LEFT_PAREN)
    elif c == ')': self.add_null_token(TokenType.RIGHT_PAREN)
    elif c == '{': self.add_null_token(TokenType.LEFT_BRACE)
    elif c == '}': self.add_null_token(TokenType.RIGHT_BRACE)
    elif c == ',': self.add_null_token(TokenType.COMMA)
    elif c == '.': self.add_null_token(TokenType.DOT)
    elif c == '-': self.add_null_token(TokenType.MINUS)
    elif c == '+': self.add_null_token(TokenType.PLUS)
    elif c == ';': self.add_null_token(TokenType.SEMICOLON)
    elif c == '*': self.add_null_token(TokenType.STAR)
    elif c == '!': self.add_null_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
    elif c == '=': self.add_null_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
    elif c == '<': self.add_null_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
    elif c == '>': self.add_null_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
    elif c == '/':
      if self.match('/'):
        while self.peek() != '\n' and not self.is_at_end():
          self.advance()
      else:
        self.add_null_token(TokenType.SLASH)
    elif c in ' \t\r': pass
    elif c == '\n': self.line += 1
    elif c == '"': self.string()
    else:  
      if self.is_digit(c):
        self.number()
      elif self.is_alpha(c):
        self.identifier()
      else:
        scanner_error(self.line, "Unexpected character.")

  def identifier(self) -> None:
    while self.is_alphanumeric(self.peek()): self.advance()

    text = self.source[self.start:self.current]
    type = keywords.get(text)
    if type == None: type = TokenType.IDENTIFIER
    
    self.add_null_token(type)


  def is_alpha(self, c: str) -> bool:
    return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'

  def is_digit(self, c: str) -> bool:
    return c >= '0' and c <= '9'
  
  def is_alphanumeric(self,c: str) -> bool:
    return self.is_alpha(c) or self.is_digit(c)
  
  def number(self) -> None:
    while self.is_digit(self.peek()): self.advance()

    if self.peek() == '.' and self.is_digit(self.peek_next()):
        self.advance()
        while self.is_digit(self.peek()): self.advance()


    self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))


  def string(self) -> None:
    while self.peek() != '"' and not self.is_at_end():
      if self.peek() == '\n': self.line += 1
      self.advance()

    if self.is_at_end():
      scanner_error(self.line, "Unterminated string.")
      return
    
    self.advance()

    value = self.source[self.start+1:self.current-1]
    self.add_token(TokenType.STRING, value)

  def peek(self) -> str:
    if self.is_at_end(): return '\0'
    return self.source[self.current]
  
  def peek_next(self) -> str:
    if self.current+1 >= len(self.source): return '\0'
    return self.source[self.current+1]

  def match(self, expected: str) -> bool:
    if self.is_at_end(): return False
    if self.source[self.current] != expected: return False

    self.current += 1
    return True

  def advance(self) -> str:
    tmp = self.source[self.current]
    self.current += 1
    return tmp

  def add_null_token(self, type: TokenType) -> None:
    self.add_token(type, None)

  def add_token(self, type: TokenType, literal: Any) -> None:
    text = self.source[self.start:self.current]
    self.tokens.append(Token(type, text, literal, self.line))

  def is_at_end(self) -> bool:
    return self.current >= len(self.source)
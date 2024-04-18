import sys
from lox import Token, TokenType

had_error = False

def scanner_error(line: int, message: str) -> None:
  report(line, '', message)

def parser_error(token: Token, message: str) -> None:
  if token.type == TokenType.EOF:
    report(token.line, " at end", message)
  else:
    report(token.line, f" at '{token.lexeme,}'", message)

def report(line: int, where: str, message: str) -> None:
  global had_error
  
  print(f'[line {line}] Error{where}: {message}', file=sys.stderr)
  had_error = True

def run(source) -> None:
  from .scanner import Scanner
  from .parser import Parser
  from .ast_printer import AstPrinter

  scanner = Scanner(source)
  tokens = scanner.scan_tokens()
  parser = Parser(tokens)
  expression = parser.parse()

  if had_error: return

  print(AstPrinter().print(expression))

def run_file(filename) -> None:
  global had_error

  with open(filename, 'r') as f:
    source = f.read()
  run(source)

  if had_error:
    sys.exit(65)

def run_prompt() -> None:
  global had_error

  while True:
    line = input("> ")
    if not line:
      break
    run(line)
    had_error = False


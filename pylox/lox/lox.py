import sys
from . import Token, TokenType

had_error = False
had_runtime_error = False

def runtime_error(error):
  print(f'{str(error)}\n[line: {error.token.line}]', file=sys.stderr)
  had_runtime_error = True

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
  from .interpreter import Interpreter


  scanner = Scanner(source)
  interpreter = Interpreter()
  tokens = scanner.scan_tokens()
  parser = Parser(tokens)
  statements = parser.parse()

  if had_error: return

  interpreter.interpret(statements)

def run_file(filename) -> None:
  global had_error

  with open(filename, 'r') as f:
    source = f.read()
  run(source)

  if had_error:
    sys.exit(65)

  if had_runtime_error:
    sys.exit(70)

def run_prompt() -> None:
  global had_error

  while True:
    line = input("> ")
    if not line:
      break
    run(line)
    had_error = False


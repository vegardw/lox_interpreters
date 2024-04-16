import sys

had_error = False

def error(line: int, message: str) -> None:
  report(line, '', message)

def report(line: int, where: str, message: str) -> None:
  global had_error
  
  print(f'[line {line}] Error{where}: {message}', file=sys.stderr)
  had_error = True

def run(source) -> None:
  from .scanner import Scanner
  scanner = Scanner(source)
  tokens = scanner.scan_tokens()

  for token in tokens:
    print(token)

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


#!/usr/bin/env python
import sys
from lox import *


def main(argv) -> None:
  if len(argv) > 2:
    print("Usage: pylox [script]")
    sys.exit(64)
  elif len(argv) == 2:
    run_file(argv[1])
  else:
    run_prompt()
    

if __name__ == "__main__":
  main(sys.argv)

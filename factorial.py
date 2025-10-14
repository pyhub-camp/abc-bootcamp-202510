#!/usr/bin/env python3
"""
Factorial calculator

Usage:
  python factorial.py 5
  python factorial.py   # then enter a number when prompted
"""

from __future__ import annotations

import argparse
import sys


def factorial(n: int) -> int:
    """Return n! for a non-negative integer n.

    Raises:
        TypeError: if n is not an int
        ValueError: if n is negative
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute factorial of a non-negative integer")
    parser.add_argument("n", nargs="?", type=int, help="Non-negative integer")
    args = parser.parse_args(argv)

    if args.n is None:
        try:
            raw = input("Enter a non-negative integer: ").strip()
        except EOFError:
            print("No input provided.", file=sys.stderr)
            return 2
        if raw == "":
            print("No input provided.", file=sys.stderr)
            return 2
        try:
            n = int(raw)
        except ValueError:
            print("Invalid integer.", file=sys.stderr)
            return 2
    else:
        n = args.n

    try:
        value = factorial(n)
    except (TypeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    print(value)
    return 0


if __name__ == "__main__":
    sys.exit(main())


from helpers import validate
from py2mojo.rules import RuleSet


def test_fibonacci():
    validate(
        '''
def fib(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    """
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)
''',
        '''
def fib(n: Int) -> Int:
    """
    Calculate the nth Fibonacci number.
    """
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)
''',
    )
    validate(
        '''
def fib(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    """
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)
''',
        '''
fn fib(n: Int) -> Int:
    """
    Calculate the nth Fibonacci number.
    """
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)
''',
        rules=RuleSet(convert_def_to_fn=True),
    )

from helpers import validate


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
        level=1,
    )

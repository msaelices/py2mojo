import sys

from py2mojo.main import convert_to_mojo


def _validate(source: str, expected: str) -> None:
    annotated_source = convert_to_mojo(source)
    assert annotated_source == expected


def test_convert_assignments():
    _validate(
        'x: int = 10',
        'var x: Int = 10',
    )
    _validate(
        'x: float = 10.5',
        'var x: Float64 = 10.5',
    )
    _validate(
        'x: List[int] = []',
        'var x: List[Int] = []',
    )
    _validate(
        'x: list[float] = []',
        'var x: list[Float64] = []',
    )
    _validate(
        'x: str = "foo"',
        'x: str = "foo"',  # no changed
    )

def test_convert_functiondefs():
    _validate(
        'def reverse(l: list[int]) -> list[int]: return reversed(l)',
        'def reverse(l: list[Int]) -> list[Int]: return reversed(l)',
    )
    _validate(
        'def add(x: int, y: int) -> int: return x + y',
        'def add(x: Int, y: Int) -> Int: return x + y',
    )
    _validate(
        'def concat(l1: list[int], l2: list[int]) -> int: return l1 + l2',
        'def concat(l1: list[Int], l2: list[Int]) -> Int: return l1 + l2',
    )
    _validate(
        'def concat(l1: list[float], l2: list[float]) -> list[float]: return l1 + l2',
        'def concat(l1: list[Float64], l2: list[Float64]) -> list[Float64]: return l1 + l2',
    )
    _validate(
        'def concat(l1: list, l2: list) -> list: return l1 + l2',
        'def concat(l1: list, l2: list) -> list: return l1 + l2',  # no changed
    )

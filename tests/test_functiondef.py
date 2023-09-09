from helpers import validate


def test_functiondef_with_basic_types():
    validate(
        'def add(x: int, y: int) -> int: return x + y',
        'def add(x: Int, y: Int) -> Int: return x + y',
    )
    validate(
        'def add(x: float, y: float) -> float: return x + y',
        'def add(x: Float64, y: Float64) -> Float64: return x + y',
    )


def test_functiondef_with_list_types():
    validate(
        'def reverse(l: list[int]) -> list[int]: return reversed(l)',
        'def reverse(l: list[Int]) -> list[Int]: return reversed(l)',
    )
    validate(
        'def concat(l1: list[int], l2: list[int]) -> int: return l1 + l2',
        'def concat(l1: list[Int], l2: list[Int]) -> Int: return l1 + l2',
    )
    validate(
        'def concat(l1: list[float], l2: list[float]) -> list[float]: return l1 + l2',
        'def concat(l1: list[Float64], l2: list[Float64]) -> list[Float64]: return l1 + l2',
    )
    validate(
        'def concat(l1: list, l2: list) -> list: return l1 + l2',
        'def concat(l1: list, l2: list) -> list: return l1 + l2',  # no changed
    )


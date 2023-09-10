import pytest

from helpers import validate

# parametrize the converted types
@pytest.mark.parametrize(
    'python_type, mojo_type',
    [
        ('int', 'Int'),
        ('float', 'Float64'),
    ]
)
def test_functiondef_with_basic_types(python_type, mojo_type):
    validate(
        f'def add(x: {python_type}, y: {python_type}) -> {python_type}: return x + y',
        f'def add(x: {mojo_type}, y: {mojo_type}) -> {mojo_type}: return x + y',
    )
    validate(
        f'def add(x: {python_type}, y: {python_type}) -> {python_type}: return x + y',
        f'fn add(x: {mojo_type}, y: {mojo_type}) -> {mojo_type}: return x + y',
        level=1,
    )


@pytest.mark.parametrize(
    'python_type, mojo_type',
    [
        ('int', 'Int'),
        ('float', 'Float64'),
    ]
)
def test_functiondef_with_list_types(python_type, mojo_type):
    validate(
        f'def flatten(l1: list[list[{python_type}]]) -> list[{python_type}]: ...',
        f'def flatten(l1: list[list[{mojo_type}]]) -> list[{mojo_type}]: ...',
    )
    validate(
        f'def reverse(l: list[{python_type}]) -> list[{python_type}]: return reversed(l)',
        f'def reverse(l: list[{mojo_type}]) -> list[{mojo_type}]: return reversed(l)',
    )
    validate(
        f'def concat(l1: list[{python_type}], l2: list[{python_type}]) -> {python_type}: return l1 + l2',
        f'def concat(l1: list[{mojo_type}], l2: list[{mojo_type}]) -> {mojo_type}: return l1 + l2',
    )
    validate(
        'def concat(l1: list, l2: list) -> list: return l1 + l2',
        'def concat(l1: list, l2: list) -> list: return l1 + l2',  # no changed
    )

def test_functiondef_inside_classes():
    validate(
'''
class Point:
    def __init__(self, x: int, y: int) -> int: ...
''',
'''
class Point:
    def __init__(inout self, x: Int, y: Int) -> Int: ...
''',
    )

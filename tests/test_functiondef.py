import pytest

from helpers import validate
from py2mojo.exceptions import ParseException
from py2mojo.rules import RuleSet


def test_functiondef_with_no_params():
    validate(
        'def main(): print("Hello world!")',
        'def main(): print("Hello world!")',
    )
    validate(
        'def main(): print("Hello world!")',
        'fn main(): print("Hello world!")',
        rules=RuleSet(convert_def_to_fn=True),
    )


@pytest.mark.parametrize(
    'python_type, mojo_type',
    [
        ('int', 'Int'),
        ('float', 'Float64'),
    ],
)
def test_functiondef_with_basic_types(python_type, mojo_type):
    validate(
        f'def add(x: {python_type}, y: {python_type}) -> {python_type}: return x + y',
        f'def add(x: {mojo_type}, y: {mojo_type}) -> {mojo_type}: return x + y',
    )
    validate(
        f'def add(x: {python_type}, y: {python_type}) -> {python_type}: return x + y',
        f'fn add(x: {mojo_type}, y: {mojo_type}) -> {mojo_type}: return x + y',
        rules=RuleSet(convert_def_to_fn=True),
    )


@pytest.mark.parametrize(
    'python_type, mojo_type',
    [
        ('int', 'Int'),
        ('float', 'Float64'),
    ],
)
def test_functiondef_with_list_types(python_type, mojo_type):
    validate(
        f'def flatten(l1: list[list[{python_type}]]) -> list[{python_type}]: ...',
        f'def flatten(l1: List[List[{mojo_type}]]) -> List[{mojo_type}]: ...',
    )
    validate(
        f'def reverse(l: list[{python_type}]) -> list[{python_type}]: return reversed(l)',
        f'def reverse(l: List[{mojo_type}]) -> List[{mojo_type}]: return reversed(l)',
    )
    validate(
        f'def concat(l1: list[{python_type}], l2: list[{python_type}]) -> {python_type}: return l1 + l2',
        f'def concat(l1: List[{mojo_type}], l2: List[{mojo_type}]) -> {mojo_type}: return l1 + l2',
    )
    validate(
        'def concat(l1: list, l2: list) -> list: return l1 + l2',
        'def concat(l1: List, l2: List) -> List: return l1 + l2',  # no changed
    )


def test_functiondef_with_float_in_precision():
    validate(
        'def add(x: float, y: float) -> float: return x + y',
        'fn add(x: Float32, y: Float32) -> Float32: return x + y',
        rules=RuleSet(convert_def_to_fn=True, float_precision=32),
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


def test_functiondef_non_fully_annotated_functions():
    validate(
        '''def add(x, y): return x + y''',
        '''def add(x, y): return x + y''',
    )
    with pytest.raises(ParseException):
        validate(
            '''def add(x, y): return x + y''',
            '''def add(x, y): return x + y''',
            rules=RuleSet(convert_def_to_fn=True),
        )

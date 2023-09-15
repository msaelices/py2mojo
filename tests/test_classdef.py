import pytest

from helpers import validate
from py2mojo.exceptions import ParseException
from py2mojo.rules import RuleSet


def test_classdef():
    validate(
        'class Foo(Bar): pass',
        'class Foo(Bar): pass',
    )
    validate(
        'class Foo(Bar): pass',
        'struct Foo(Bar): pass',
        rules=RuleSet(convert_class_to_struct=True),
    )
    validate(
        'class Foo(Bar): n: int = 10',
        'struct Foo(Bar): var n: Int = 10',
        rules=RuleSet(convert_class_to_struct=True),
    )


def test_classdef_non_fully_annotated_classes():
    validate(
        '''class Number: number = 10''',
        '''class Number: number = 10''',
        rules=RuleSet(convert_class_to_struct=False),
    )
    with pytest.raises(ParseException):
        validate(
            '''class Number: number = 10''',
            '''class Number: number = 10''',
            rules=RuleSet(convert_class_to_struct=True),
        )

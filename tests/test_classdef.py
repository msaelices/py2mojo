from helpers import validate
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

from helpers import validate


def test_classdef():
    validate(
        'class Foo(Bar): pass',
        'class Foo(Bar): pass',
    )
    validate(
        'class Foo(Bar): pass',
        'struct Foo(Bar): pass',
        level=1
    )

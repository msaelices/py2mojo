import sys

from py2mojo.main import convert_to_mojo


def _validate(source: str, expected: str) -> None:
    annotated_source = convert_to_mojo(source)
    assert annotated_source == expected


def test_convert_integer():
    _validate(
        'x: int = 10',
        'var x: Int = 10',
    )
    _validate(
        'x: str = "foo"',
        'x: str = "foo"',  # no changed
    )

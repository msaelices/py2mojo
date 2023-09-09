from py2mojo.main import convert_to_mojo


def validate(source: str, expected: str) -> None:
    converted_source = convert_to_mojo(source)
    assert converted_source == expected

from py2mojo.main import convert_to_mojo


def validate(source: str, expected: str, level: int = 0) -> None:
    converted_source = convert_to_mojo(source, level=level)
    assert converted_source == expected

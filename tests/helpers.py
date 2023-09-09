from py2mojo.main import convert_to_mojo


def validate(source: str, expected: str) -> None:
    annotated_source = convert_to_mojo(source)
    assert annotated_source == expected

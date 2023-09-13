from py2mojo.main import convert_to_mojo
from py2mojo.rules import RuleSet


def validate(source: str, expected: str, rules: RuleSet | None = None) -> None:
    rules = rules or RuleSet()
    converted_source = convert_to_mojo(source, rules=rules)
    assert converted_source == expected

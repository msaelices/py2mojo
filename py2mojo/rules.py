import argparse
from dataclasses import dataclass


@dataclass
class RuleSet:
    convert_def_to_fn: bool = False
    convert_class_to_struct: bool = False
    float_precision: int = 64


def get_rules(args: argparse.Namespace) -> RuleSet:
    return RuleSet(
        convert_def_to_fn=args.convert_def_to_fn,
        convert_class_to_struct=args.convert_class_to_struct,
        float_precision=args.float_precision,
    )

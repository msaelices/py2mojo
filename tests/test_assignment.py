from helpers import validate


def test_assignment_with_basic_types():
    validate(
        'x: int = 10',
        'var x: Int = 10',
    )
    validate(
        'x: float = 10.5',
        'var x: Float64 = 10.5',
    )
    validate(
        'x: str = "foo"',
        'var x: str = "foo"',
    )
    validate(
        'x: int',
        'var x: Int',
    )
    validate(
        '"""docstring"""\nx: int',
        '"""docstring"""\nvar x: Int',
    )


def test_assignment_with_list_types():
    validate(
        'x: List[int] = []',
        'var x: List[Int] = []',
    )
    validate(
        'x: list[float] = []',
        'var x: list[Float64] = []',
    )
    validate(
        'x: list = []',
        'var x: list = []',
    )

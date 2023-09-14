import ast


class ParseException(Exception):
    def __init__(self, node: ast.AST, msg: str):
        self.node = node
        self.msg = msg

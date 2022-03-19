class Token:
    def __init__(self, lexeme, type) -> None:
        self.lexeme = lexeme
        self.type = type

    def __repr__(self) -> str:
        return f"({self.lexeme}, {self.type})"

class InvalidSyntaxError(Exception):
    def __init__(self, start_position, end_position, details=""):
        super().__init__(start_position, end_position, "Invalid syntax", details)

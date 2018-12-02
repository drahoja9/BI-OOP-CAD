import abc


class ParseResult:
    """
    Describes the result of parsing. Every method of any parser should return
    one of ParseResult's subtypes.
    """
    def __init__(self, expected):
        self.expected = expected

    @abc.abstractmethod
    def has_remainder(self) -> bool:
        return

    @abc.abstractmethod
    def is_successful(self) -> bool:
        return

    @abc.abstractmethod
    def print(self):
        return


class Success(ParseResult):
    """
    Indicates that parsing was successful.
    Contains information about expected result of parsing and
    a remainder of the parsed input.
    """
    def __init__(self, expected, remainder):
        super().__init__(expected)
        self.remainder = remainder

    def has_remainder(self):
        if len(self.remainder) > 0:
            return True
        else:
            return False

    def is_successful(self):
        return True

    def print(self):
        remainder_str = ', '.join(self.remainder)
        return "Suceesfully matched \"" + self.expected + "\", remainder is \"" + remainder_str + "\""


class Failure(ParseResult):
    """
    Indicates that parsing failed. Contains information about
    expected result of parsing and actual result of parsing.
    """
    def __init__(self, expected, actual):
        super().__init__(expected)
        self.actual = actual

    def has_remainder(self):
        return NotImplementedError

    def is_successful(self):
        return False

    def print(self):
        return "Expected \"" + self.expected + "\", got \"" + self.actual + "\""

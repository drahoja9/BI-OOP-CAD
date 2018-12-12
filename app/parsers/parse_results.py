import abc


class ParseResult:
    """
    Describes the result of parsing. Every method of any parser should return
    one of ParseResult's subtypes.

    :param expected: expected object
    """
    def __init__(self, expected):
        self.expected = expected

    def get_expected(self):
        return self.expected

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

    :param remainder: the input remainder
    """
    def __init__(self, expected, remainder):
        super().__init__(expected)
        self.remainder = remainder

    def __eq__(self, other):
        return self.expected == self.expected and self.remainder == other.remainder

    def has_remainder(self):
        if len(self.remainder) > 0:
            return True
        else:
            return False

    def get_remainder(self):
        return self.remainder

    def is_successful(self):
        return True

    def print(self):
        remainder_str = ''.join(self.remainder)
        return "Suceesfully matched \"" + self.expected + "\", remainder is \"" + remainder_str + "\""


class Failure(ParseResult):
    """
    Indicates that parsing failed. Contains information about
    expected result of parsing and actual result of parsing.

    :param actual: actual string that was parsed from the input
    """
    def __init__(self, expected, actual):
        super().__init__(expected)
        self.actual = actual

    def get_actual(self):
        return self.actual

    def is_successful(self):
        return False

    def print(self):
        return "Expected \"" + self.expected + "\", got \"" + self.actual + "\""

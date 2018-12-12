import abc


class ParseResult:
    """
    Describes the result of parsing. Every method of any parser should return
    one of ParseResult's subtypes.
    """
    @abc.abstractmethod
    def is_successful(self) -> bool:
        return

    @abc.abstractmethod
    def print(self):
        return


class Success(ParseResult):
    """
    Indicates that parsing has been successful.
    Contains the matched object parsed from input and a remainder of the parsed input.

    :param match: the matched object
    :param remainder: the input remainder
    """
    def __init__(self, match, remainder):
        self.match = match
        self.remainder = remainder

    def __eq__(self, other):
        return self.match == self.match and self.remainder == other.remainder

    def get_match(self):
        return self.match

    def has_remainder(self):
        if len(self.remainder) > 0:
            return True
        else:
            return False

    def get_remainder(self):
        return self.remainder

    def is_successful(self):
        return True

    "TODO: tady bude potreba neco jako 'match.toString'"
    def print(self):
        remainder_str = ''.join(self.remainder)
        return "Successfully matched \"" + self.match + "\", remainder is \"" + remainder_str + "\""


class Failure(ParseResult):
    """
    Indicates that parsing has failed. Contains expected result of parsing
    and the actual result of parsing.

    :param expected: expected string
    :param actual: actual string that was parsed from the input
    """
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual

    def get_expected(self):
        return self.expected

    def get_actual(self):
        return self.actual

    def is_successful(self):
        return False

    def print(self):
        return "Expected \"" + self.expected + "\", got \"" + self.actual + "\""

import abc


class ParseResult:
    """
    Describes the result of parsing. Every method of any parser should return
    one of ParseResult's subtypes.
    """
    def __eq__(self, other):
        return self.__class__ == other.__class__

    @abc.abstractmethod
    def is_successful(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def print(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_match(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_remainder(self):
        raise NotImplementedError


class Success(ParseResult):
    """
    Indicates that parsing has been successful.
    Contains the matched object parsed from input and a remainder of the parsed input.

    :param match: the matched object
    :param remainder: the input remainder
    """
    def __init__(self, match: object, remainder: str):
        self._match = match
        self._remainder = remainder

    def __eq__(self, other):
        return super().__eq__(other) and \
               self._match.__eq__(other.get_match()) and self._remainder.__eq__(other.get_remainder())

    def get_match(self):
        return self._match

    def has_remainder(self):
        if len(self._remainder) > 0:
            return True
        else:
            return False

    def get_remainder(self):
        return self._remainder

    def is_successful(self):
        return True

    def print(self):
        remainder_str = ''.join(self._remainder)
        return "Successfully matched \"" + self._match.__repr__() + "\", remainder is \"" + remainder_str + "\""

    def __repr__(self):
        remainder_str = ''.join(self._remainder)
        return "Success(" + self._match.__repr__() + ", \"" + remainder_str + "\")"


class Failure(ParseResult):
    """
    Indicates that parsing has failed. Contains expected result of parsing
    and the actual result of parsing.

    :param expected: expected string
    :param actual: actual string that was parsed from the input
    """
    def __init__(self, expected: str, actual: str):
        self._expected = expected
        self._actual = actual

    def __eq__(self, other):
        return super().__eq__(other) and \
               self._expected == other.get_expected() and self._actual.__eq__(other.get_actual())

    def get_expected(self):
        return self._expected

    def get_actual(self):
        return self._actual

    def get_remainder(self):
        raise NotImplementedError

    def get_match(self):
        raise NotImplementedError

    def is_successful(self):
        return False

    def print(self):
        return "Expected \"" + self._expected + "\", got \"" + self._actual + "\""

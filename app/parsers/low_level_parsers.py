import re

from app.parsers.parse_results import ParseResult, Success, Failure


class LowLevelParser:
    def __init__(self, expected: str, delimiter: str = ''):
        """
        :param expected: string, should be escaped unless it's a regular expression
        :param delimiter: string, is matched after the expected expression
        """
        self._expected = expected
        self._delimiter = delimiter

    def parse_input(self, cli_input: str) -> ParseResult:
        if self._delimiter == '':
            match = re.match(r'^(\s*)(' + self._expected + ')(\s+|$)', cli_input)
        else:
            match = re.match(r'^(\s*)(' + self._expected + ')' +
                             r'(\s*)' + re.escape(self._delimiter) + r'(\s*|$)', cli_input)

        if match:
            remainder = cli_input[match.end():]
            return Success(match.group(2), remainder)
        else:
            return Failure(self._expected, cli_input)


class WordParser(LowLevelParser):
    def __init__(self):
        super().__init__('\w+')


class StringParser(LowLevelParser):
    """
    Parser used for parsing expected strings from the beginning of the input.
    """
    def __init__(self, expected: str, delimiter: str = ''):
        super().__init__(re.escape(expected), delimiter)


class NumberParser(LowLevelParser):
    """
    Parser used for parsing numbers from the beginning of the input.
    """
    def __init__(self, expected: str, delimiter: str = ''):
        super().__init__(expected, delimiter)

    def parse_input(self, cli_input: str):
        result = super().parse_input(cli_input)
        if result.is_successful():
            integer = int(result.get_match())
            return Success(integer, result.get_remainder())

        return result


class NatParser(NumberParser):
    """
    Parser used for parsing natural numbers from the beginning of given input.
    Natural number is just a number without a sign.
    """
    def __init__(self, delimiter: str = ''):
        super().__init__(r'\d+', delimiter)


class IntParser(NumberParser):
    """
    Parser used for parsing integers from the beginning of given input.
    Integer is a number with a positive or negative sign (+-).
    """
    def __init__(self, delimiter: str = ''):
        super().__init__(r'[+-]\d+', delimiter)

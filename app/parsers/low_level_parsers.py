import re
from app.parsers.parse_results import *


class StringParser:
    def parse_string(self, expected: str, cli_input: str, delimiter: str) -> ParseResult:
        """
        Parse a word from the beginning of given input with given delimiter.
        If delimiter is empty, the given input needs to be equal to expected input.
        :param expected: expected word
        :param cli_input: string
        :param delimiter: string
        :return: Success(matched string, remainder) if input contains expected word,
        Failure(expected string, actual string) otherwise
        """
        if delimiter == '':
            match = re.match(r'^(' + re.escape(expected) + r')$', cli_input)
        else:
            match = re.match(r'^(' + re.escape(expected) + r')' + re.escape(delimiter), cli_input)

        if match:
            string = match.group(1)
            remainder = cli_input[match.end():]
            return Success(string, remainder)
        else:
            return Failure(expected, cli_input)


class NumberParser:
    def parse_number(self, cli_input: str, delimiter1: str, delimiter2: str) -> ParseResult:
        """
        Parse a number with each of both given delimiters from the given CLI input.
        :param cli_input: string
        :param delimiter1: string First delimiter
        :param delimiter2: string Second delimiter
        :return: Success(integer or natural number, remainder) if input contains either valid integer or
        natural number within range, Failure(expected format, the given cli_input) otherwise
        """

        # Parse a number from the given input using the first given delimiter
        result1 = self.parse_input(cli_input, delimiter1)
        if result1.is_successful():
            return result1

        if delimiter1 != delimiter2:
            # Parse a number from the given input using the second given delimiter
            result2 = self.parse_input(cli_input, delimiter2)
            if result2.is_successful():
                return result2

        # Parsing a number has failed for both delimiters (or for the first one if both delimiters are the same),
        # return Failure result from the first parser
        return result1

    @abc.abstractmethod
    def parse_input(self, cli_input: str, delimiter: str) -> ParseResult:
        raise NotImplementedError


class NatParser(NumberParser):
    def parse_input(self, cli_input: str, delimiter: str) -> ParseResult:
        """
        Parse natural number from the beginning of given input.
        Natural number is just a number without a sign.
        :param cli_input: string
        :param delimiter: string Delimits the matched natural number and the remainder
        :return: Success(matched nat. number, remainder) if input contains valid natural number within range,
        Failure(expected format, the given cli_input) otherwise
        """
        if delimiter == '':
            match = re.match(r'^(\d+)$', cli_input)
        else:
            match = re.match(r'^(\d+)' + re.escape(delimiter), cli_input)

        if match:
            nat = int(match.group(1))
            remainder = cli_input[match.end():]
            return Success(nat, remainder)
        else:
            return Failure("a natural number", cli_input)


class IntParser(NumberParser):
    def parse_input(self, cli_input: str, delimiter: str) -> ParseResult:
        """
        Parse integer from the beginning of given input.
        Integer is a number with a positive or negative sign (+-)
        :param cli_input: string
        :param delimiter: string Delimits the matched integer and the remainder
        :return: Success(matched integer, remainder) if input contains valid integer within range,
        Failure(expected format, the given cli_input) otherwise
        """
        if delimiter == '':
            match = re.match(r'^([+-]\d+)$', cli_input)
        else:
            match = re.match(r'^([+-]\d+)' + re.escape(delimiter), cli_input)

        if match:
            nat = int(match.group(1))
            remainder = cli_input[match.end():]
            return Success(nat, remainder)
        else:
            return Failure("an integer", cli_input)

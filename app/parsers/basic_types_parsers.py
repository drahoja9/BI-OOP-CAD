import re
from app.parsers.parse_results import *


class StringParser:
    def parse_string(self, expected, cli_input) -> ParseResult:
        """
        Parse word from the beginning of given input.
        Remaining string is split by spaces into a list.
        :param expected: expected word
        :param cli_input: string
        :return: Success(string, string) if input contains expected word,
        Failure(string, string) otherwise
        """
        cli_input = cli_input.split()  # split words separated by space to list
        if expected == cli_input[0]:
            cli_input.pop(0)
            return Success(expected, cli_input)
        else:
            return Failure(expected, cli_input[0])


class NatParser:
    def parse_nat(self, cli_input) -> ParseResult:
        """
        Parse natural number from the beginning of given input.
        Natural number is just a number without a sign.
        :param cli_input: string
        :return: Success(int, string) if input contains valid natural number within range,
        Failure(string, string) otherwise
        """
        match = re.search(r'^\d+(\s+|$)', cli_input)
        if match:
            # if there is a space after matched integer, ignore it
            if cli_input[match.end()-1:match.end()] == ' ':
                nat = int(cli_input[match.start():match.end() - 1])
            else:
                nat = int(cli_input[match.start():match.end()])

            remainder = cli_input[match.end():(len(cli_input))]
            return Success(nat, remainder)
        else:
            return Failure("a natural number", cli_input)


class IntParser:
    def parse_integer(self, cli_input) -> ParseResult:
        """
        Parse integer from the beginning of given input.
        Integer is a number with a positive or negative sign (+-).
        :param cli_input: string
        :return: Success(int, string) if input contains valid integer within range,
        Failure(string, string) otherwise.
        """
        match = re.search(r'^[-+]\d+(\s+|$)', cli_input)
        if match:
            # if there is a space after matched integer, ignore it
            if cli_input[match.end()-1:match.end()] == ' ':
                integer = int(cli_input[match.start():match.end() - 1])
            else:
                integer = int(cli_input[match.start():match.end()])

            remainder = cli_input[match.end():(len(cli_input))]
            return Success(integer, remainder)
        else:
            return Failure("an integer", cli_input)

from app.parsers.parse_results import *


class StringParser:
    def parse_string(self, expected, input) -> ParseResult:
        """
        Parse word from the beginning of given input.
        :param expected: expected word
        :param input: string
        :return: Success if input containts expected word,
        Failure otherwise
        """
        input = input.split() # split words separated by space to list
        if expected == input[0]:
            input.pop(0)
            return Success(expected, input)
        else:
            return Failure(expected, input[0])


class IntParser:
    def parse_integer(self, input) -> ParseResult:
        """
        Parse integer from the beginning of given input.
        :param input: string
        :return: Success if input contains valid integer within range,
        Failure otherwise
        """
        return NotImplementedError


class NatParser:
    def parse_nat(self, input) -> ParseResult:
        """
        Parse natural number from the beginning of given input.
        :param input: string
        :return: Success if input contains valid natural number within range,
        Failure otherwise
        """
        return NotImplementedError

from app.parsers.basic_types_parsers import *


class AbsPointParser:
    def parse_input(self, nat_parser, input) -> ParseResult:
        """ 
        Parse absolute point from input.
        :param nat_parser: NatParser
        :param input: string
        :return: Success if input contains natural number within
        range, Failure otherwise
        """
        return NotImplementedError


class RelPointParser:
    def parse_input(self, int_parser, input) -> ParseResult:
        """
        Parse relative point from input.
        :param int_parser: IntParser
        :param input: string
        :return: ParseResult - Success if input contains integer within
        range, Failure otherwise
        """
        return NotImplementedError

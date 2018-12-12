from app.parsers.basic_types_parsers import *
from app.utils import Point


class AbsPointParser:
    def parse_input(self, nat_parser, cli_input) -> ParseResult:
        """ 
        Parse absolute point from input, e.g. '10,20'.
        :param nat_parser: NatParser
        :param cli_input: string
        :return: Success(Point, string) if input contains natural number within
        range, Failure(string, string) otherwise
        """
        self.point = "TODO"
        return NotImplementedError

    def get_point(self):
        return self.point


class RelPointParser:
    def parse_input(self, int_parser, cli_input) -> ParseResult:
        """
        Parse relative point from input, e.g. '+10,-12'.
        :param int_parser: IntParser
        :param cli_input: string
        :return: Success(Point, string) if input contains integer within
        range, Failure(string, string) otherwise
        """
        self.point = "TODO"
        return NotImplementedError

    def get_point(self):
        return self.point

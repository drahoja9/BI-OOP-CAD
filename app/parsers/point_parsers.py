import abc

from app.parsers.low_level_parsers import NatParser, IntParser, NumberParser
from app.parsers.parse_results import ParseResult, Success, Failure


class PointParser:
    @staticmethod
    def parse_point(cli_input: str):
        """
        Parse either a relative point from input, e.g. '+10,-12' OR an absolute point
        from input, e.g. '10,20'.
        :param cli_input: string
        :return Success(AbsoluteParserPoint or RelativeParserPoint, remainder) if input contains either valid
        absolute point or relative point, Failure(expected format, the given cli_input) otherwise
        """
        first_nat_parser = NatParser(',')
        second_nat_parser = NatParser()
        first_int_parser = IntParser(',')
        second_int_parser = IntParser()

        # Parse absolute point from given input
        abs_point_parse = PointParser().parse_input(first_nat_parser, second_nat_parser, cli_input)
        if abs_point_parse.is_successful():
            abs_point = AbsoluteParserPoint(abs_point_parse.get_match()[0], abs_point_parse.get_match()[1])
            return Success(abs_point, abs_point_parse.get_remainder())

        # Parse relative point from given input
        rel_point_parse = PointParser().parse_input(first_int_parser, second_int_parser, cli_input)
        if rel_point_parse.is_successful():
            rel_point = RelativeParserPoint(rel_point_parse.get_match()[0], rel_point_parse.get_match()[1])
            return Success(rel_point, rel_point_parse.get_remainder())

        # Both parsers has failed to parse a point, return the last result (a Failure object)
        return rel_point_parse

    @staticmethod
    def parse_input(first_parser: NumberParser, second_parser: NumberParser, cli_input: str) -> ParseResult:
        """ 
        Parse point from input using given NumberParsers. Both NumberParser must be of the same type!
        :param first_parser: NumberParser
        :param second_parser: NumberParser
        :param cli_input: string
        :return: Success([X coordinate, Y coordinate], string) if input contains a number within
        range, Failure(string, string) otherwise
        """

        # Both given NumberParsers must be of the same type
        if first_parser.__class__ != second_parser.__class__:
            raise ValueError("first_pasrser and second_parser must be of the same type!")

        # Parse a number using comma and only comma as a delimiter"
        result1 = first_parser.parse_input(cli_input)
        if result1.is_successful():
            # Parse a number using space or end of string as a delimiter"
            result2 = second_parser.parse_input(result1.get_remainder())
            if result2.is_successful():
                x = result1.get_match()
                y = result2.get_match()
                return Success([x, y], result2.get_remainder())

        return Failure('x,y or (+-)x,(+-)y', cli_input)


class ParserPoint:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @abc.abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def is_absolute(self):
        raise NotImplementedError

    @abc.abstractmethod
    def convert_to_absolute(self, predecessor):
        raise NotImplementedError


class AbsoluteParserPoint(ParserPoint):
    def __eq__(self, other):
        return super().__eq__(other) and other.is_absolute()

    def __repr__(self):
        return 'Absolute[' + str(self.x) + ', ' + str(self.y) + ']'

    def is_absolute(self):
        return True

    def convert_to_absolute(self, predecessor):
        return self


class RelativeParserPoint(ParserPoint):
    def __eq__(self, other):
        return super().__eq__(other) and not other.is_absolute()

    def __repr__(self):
        return 'Relative[' + str(self.x) + ', ' + str(self.y) + ']'

    def is_absolute(self):
        return False

    def convert_to_absolute(self, predecessor):
        x = self.x + predecessor.x
        y = self.y + predecessor.y
        return AbsoluteParserPoint(x, y)

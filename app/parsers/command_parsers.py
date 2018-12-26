from app.parsers.parse_results import *
from app.parsers.low_level_parsers import StringParser
from app.parsers.point_parsers import *

# -------- TEMPORARY COMMANDS FOR DEBUGGING ------------
class Command:
    ...

class ListCommand(Command):
    def __init__(self, *params):
        ...

class RectCommand(Command):
    def __init__(self, *params):
        ...

class InvalidCommand(Command):
    ...

class QuitCommand(Command):
    ...

# -------- /TEMPORARY COMMANDS FOR DEBUGGING ------------


class CommandParser:
    """
    Parses command from CLI input.
    If Command (and it's parameters, if there are any required) is successfully parsed,
    Success(Command, string) is returned.
    """
    def __init__(self, string_parser: StringParser):
        self.string_parser = string_parser

    @abc.abstractmethod
    def parse_command(self, cli_input: str) -> ParseResult:
        """
        Parse corresponding command from given input.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def parse_params(self, cli_input: str) -> ParseResult:
        """
        Parse command's parameters from given input.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_parameters(self) -> bool:
        raise NotImplementedError

    def convert_points(self, points: list) -> list:
        """
        Convert given points to AbsoluteParserPoints. Every RelativeParserPoint is converted
        to AbsoluteParserPoints based on its predecessor point.
        If first point in the list is relative, its predecessor is absolute point [0,0].
        :param points: list
        :return: list List of AbsoluteParserPoints
        """

        "Check if list of points is not empty"
        if not points:
            raise AttributeError

        if points[0].is_absolute():
            predecessor = points[0]
            points.pop(0)
            absolute_points = [predecessor]
        else:
            predecessor = AbsoluteParserPoint(0, 0)
            absolute_points = []

        for point in points:
            if point.is_absolute():
                absolute_points.append(point)
            else:
                point = point.convert_to_absolute(predecessor)
                absolute_points.append(point)

            predecessor = point

        return absolute_points


class ListParser(CommandParser):
    """
    Parser for "ls" (list) Command.
    """
    def __init__(self, string_parser: StringParser):
        super().__init__(string_parser)

    def parse_command(self, cli_input: str):
        result = self.string_parser.parse_string("ls", cli_input)
        return result

    def parse_params(self, cli_input: str):
        return Success("Temporary for debugging", "not implemented yet")

    def has_parameters(self):
        return True


class RectParser(CommandParser):
    """
    Parser for "rect" (Rectangle) Command.
    Definition: rect <POINT> <POINT> | rect <POINT> <NAT> <NAT>
    """
    def __init__(self, string_parser: StringParser, point_parser: PointParser,
                 nat_parser: NatParser, int_parser: IntParser):
        super().__init__(string_parser)
        self.point_parser = point_parser
        self.nat_parser = nat_parser
        self.int_parser = int_parser

    def parse_command(self, cli_input: str):
        result = self.string_parser.parse_string("rect", cli_input)
        return result

    def parse_params(self, cli_input: str) -> ParseResult:
        points_result = self.parse_points(cli_input)
        if points_result.is_successful():
            # TODO: parse Color a pak vytvořit Command pomocí CommandFactory
            abs_points = self.convert_points(points_result.get_match())
            return Success(RectCommand(abs_points), '')

        point_and_nats_result = self.parse_point_and_nats(cli_input)
        if point_and_nats_result.is_successful():
            # TODO: parse Color a pak vytvořit Command pomocí CommandFactory
            abs_points = self.convert_points([point_and_nats_result.get_match()[0]])
            return Success(RectCommand(abs_points), '')

        return Failure(points_result.get_expected() + ' | ' + point_and_nats_result.get_expected(), cli_input)

    def parse_points(self, cli_input: str) -> ParseResult:
        """
        Parse two Points from given input.
        """
        point_result1 = self.point_parser.parse_point(cli_input, self.nat_parser, self.int_parser)
        if point_result1.is_successful():
            point_result2 = self.point_parser.parse_point(point_result1.get_remainder(), self.nat_parser, self.int_parser)
            if point_result2.is_successful():
                return Success([point_result1.get_match(), point_result2.get_match()],
                               point_result2.get_remainder())

        return Failure("rect <POINT> <POINT>", cli_input)

    def parse_point_and_nats(self, cli_input: str) -> ParseResult:
        """
        Parse a Point and two Natural numbers from given input.
        """
        point_result = self.point_parser.parse_point(cli_input, self.nat_parser, self.int_parser)
        if point_result.is_successful():
            nat_result1 = self.nat_parser.parse_number(point_result.get_remainder(), ' ', ' ')
            if nat_result1.is_successful():
                nat_result2 = self.nat_parser.parse_number(nat_result1.get_remainder(), ' ', '')
                if nat_result2.is_successful():
                    return Success([point_result.get_match(),
                                    nat_result1.get_match(),
                                    nat_result2.get_match()], nat_result2.get_remainder())

        return Failure("rect <POINT> <NAT> <NAT>", cli_input)

    def has_parameters(self):
        return True


class QuitParser(CommandParser):
    """
    Parser for "quit" Command.
    """
    def __init__(self, string_parser: StringParser):
        super().__init__(string_parser)

    def parse_command(self, cli_input: str):
        result = self.string_parser.parse_string("quit", cli_input)
        if result.is_successful():
            return Success(QuitCommand, result.get_remainder())
        else:
            return result

    def parse_params(self, cli_input: str):
        return NotImplementedError

    def has_parameters(self):
        return False

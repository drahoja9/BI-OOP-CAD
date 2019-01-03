import abc

from app.parsers.parse_results import ParseResult, Success, Failure
from app.parsers.low_level_parsers import StringParser, NatParser, IntParser
from app.parsers.point_parsers import PointParser, AbsoluteParserPoint
from app.parsers.color_parser import ColorParser
from app.shape_factory import DimensionsRectFactory, DimensionsCircleFactory
from app.commands import PrintDotCommand, PrintRectCommand, PrintCircleCommand, PrintLineCommand, \
    PrintPolylineCommand, MoveShapeCommand, RemoveShapeCommand, ListShapeCommand, LoadCommand, SaveCommand, \
    ClearCommand, QuitCommand
from app.utils import Color
from app.controller import Controller


class CommandParser:
    """
    Parses command from CLI input.
    If Command (and it's parameters, if there are any required) is successfully parsed,
    Success(Command, string) is returned.
    """
    def __init__(self, controller: Controller, command: str):
        self._controller = controller
        self._command = command

    def parse_command(self, cli_input: str) -> ParseResult:
        """
        Parse a command from given input.
        """
        string_parser = StringParser(self._command)
        result = string_parser.parse_input(cli_input)
        return result

    @abc.abstractmethod
    def parse_params(self, cli_input: str) -> ParseResult:
        """
        Parse command's parameters from given input.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_parameters(self) -> bool:
        raise NotImplementedError

    @staticmethod
    def parse_two_points(cli_input: str) -> ParseResult:
        """
        Parse two Points from given input.
        """
        point_result1 = PointParser().parse_point(cli_input)
        if point_result1.is_successful():
            point_result2 = PointParser().parse_point(point_result1.get_remainder())
            if point_result2.is_successful():
                return Success([point_result1.get_match(), point_result2.get_match()], point_result2.get_remainder())

        return Failure("<POINT> <POINT>", cli_input)

    @staticmethod
    def convert_points(points: list) -> list:
        """
        Convert given points to AbsoluteParserPoints. Every RelativeParserPoint is converted
        to AbsoluteParserPoints based on its predecessor point.
        If first point in the list is relative, its predecessor is absolute point [0,0].
        :param points: list
        :return: list List of AbsoluteParserPoints
        """

        # Check if list of points is not empty
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


class ShapeCommandParser(CommandParser):
    def __init__(self, controller: Controller, command: str, nat_parser: NatParser,
                 int_parser: IntParser, color_parser: ColorParser):
        super().__init__(controller, command)
        self.nat_parser = nat_parser
        self.int_parser = int_parser
        self.color_parser = color_parser

    def parse_color(self, cli_input: str, color_parser: ColorParser) -> ParseResult:
        """
        Parse a Color from given input.
        """
        default_color = Color(0, 0, 0)
        if cli_input == '':
            return Success(default_color, '')

        color_result = color_parser.parse_color(cli_input)
        if color_result.is_successful():
            return Success(color_result.get_match(), '')

        return Failure(color_result.get_expected(), cli_input)


# ------------- Command Parsers ------------


class MoveShapeParser(CommandParser):
    """
    Parser for "move" (Move) Command.
    Definition: move <POINT> <POINT>
    """
    def parse_params(self, cli_input: str) -> ParseResult:
        result = self.parse_two_points(cli_input)
        if result.is_successful():
            abs_points = self.convert_points(result.get_match())

            start_x = abs_points[0].x
            start_y = abs_points[0].y
            end_x = abs_points[1].x
            end_y = abs_points[1].y
            return Success(MoveShapeCommand(self._controller, start_x, start_y, end_x, end_y), result.get_remainder())
        else:
            return result

    def has_parameters(self) -> bool:
        return True


class RemoveShapeParser(CommandParser):
    """
    Parser for "remove" (Remove) Command.
    Definition: remove <POINT>
    """
    def parse_params(self, cli_input: str) -> ParseResult:
        result = PointParser().parse_point(cli_input)
        if result.is_successful():
            abs_point = self.convert_points([result.get_match()])

            x = abs_point[0].x
            y = abs_point[0].y
            return Success(RemoveShapeCommand(self._controller, x, y), result.get_remainder())
        else:
            return result

    def has_parameters(self) -> bool:
        return True


class ListParser(CommandParser):
    """
    Parser for "ls" (List) Command.
    Definition: ls | ls <POINT>
    """
    def parse_params(self, cli_input: str):
        if cli_input == '':
            # point parameter is absent, return ListShapeCommand with default values of parameters x and y
            return Success(ListShapeCommand(self._controller), '')

        result = PointParser.parse_point(cli_input)
        if result.is_successful():
            abs_point = self.convert_points([result.get_match()])

            x = abs_point[0].x
            y = abs_point[0].y
            return Success(ListShapeCommand(self._controller, x, y), result.get_remainder())
        else:
            return result

    def has_parameters(self):
        return True


class ClearParser(CommandParser):
    """
    Parser for 'clear' (Clear) command.
    """
    def parse_command(self, cli_input: str) -> ParseResult:
        result = super().parse_command(cli_input)
        if result.is_successful():
            return Success(ClearCommand(self._controller), result.get_remainder())
        else:
            return result

    def parse_params(self, cli_input: str) -> ParseResult:
        raise NotImplementedError

    def has_parameters(self) -> bool:
        return False


class SaveParser(CommandParser):
    """
    Parser for 'save' (Save) command.
    Definition: save | save <STRING>
    """
    def parse_params(self, cli_input: str) -> ParseResult:
        if cli_input == '':
            return Success(SaveCommand(self._controller, None), '')
        else:
            return Success(SaveCommand(self._controller, cli_input), '')

    def has_parameters(self) -> bool:
        return True


class LoadParser(CommandParser):
    """
    Parser for 'load' (Load) command.
    Definition: load <STRING>
    """
    def parse_params(self, cli_input: str) -> ParseResult:
        if cli_input == '':
            return Success(LoadCommand(self._controller, None), '')
        else:
            return Success(LoadCommand(self._controller, cli_input), '')

    def has_parameters(self) -> bool:
        return True


class QuitParser(CommandParser):
    """
    Parser for 'quit' (Quit) command.
    Definition: quit
    """
    def parse_command(self, cli_input: str) -> ParseResult:
        result = super().parse_command(cli_input)
        if result.is_successful():
            return Success(QuitCommand(self._controller), result.get_remainder())
        else:
            return result

    def parse_params(self, cli_input: str) -> ParseResult:
        raise NotImplementedError

    def has_parameters(self) -> bool:
        return False


# ------------- Shape Command Parsers ------------


class RectParser(ShapeCommandParser):
    """
    Parser for "rect" (Rectangle) Command.
    Definition: ( rect <POINT> <POINT> | rect <POINT> <NAT> <NAT>) ) <COLOR>
    COLOR := rgb([0,255],[0,255],[0,255]) | <empty string>
    """
    def parse_params(self, cli_input: str) -> ParseResult:
        points_result = self.parse_two_points(cli_input)
        if points_result.is_successful():
            # TODO: parse Color a pak vytvořit Command pomocí CommandFactory
            abs_points = self.convert_points(points_result.get_match())

            # Parse color
            color_result = self.parse_color(points_result.get_remainder(), self.color_parser)
            if color_result.is_successful():
                start_x = abs_points[0].x
                start_y = abs_points[0].y
                end_x = abs_points[1].x
                end_y = abs_points[1].y
                return Success(PrintRectCommand(self._controller, start_x, start_y, color_result.get_match(),
                                                end_x=end_x, end_y=end_y,), '')
            else:
                return Failure(color_result.get_expected(), points_result.get_remainder())

        point_and_nats_result = self.parse_point_and_nats(cli_input)
        if point_and_nats_result.is_successful():
            width = point_and_nats_result.get_match()[1]
            height = point_and_nats_result.get_match()[2]

            abs_points = self.convert_points([point_and_nats_result.get_match()[0]])

            # Parse color
            color_result = self.parse_color(point_and_nats_result.get_remainder(), self.color_parser)
            if color_result.is_successful():
                start_x = abs_points[0].x
                start_y = abs_points[0].y
                return Success(PrintRectCommand(self._controller, start_x, start_y, color_result.get_match(),
                                                DimensionsRectFactory, width=width, height=height), '')
            else:
                return Failure(color_result.get_expected(), point_and_nats_result.get_remainder())

        return Failure(points_result.get_expected() + ' | ' + point_and_nats_result.get_expected(), cli_input)

    def parse_point_and_nats(self, cli_input: str) -> ParseResult:
        """
        Parse a Point and two Natural numbers from given input.
        """
        first_nat_parser = NatParser(' ')
        second_nat_parser = NatParser()

        point_result = PointParser().parse_point(cli_input)
        if point_result.is_successful():
            nat_result1 = first_nat_parser.parse_input(point_result.get_remainder())
            if nat_result1.is_successful():
                nat_result2 = second_nat_parser.parse_input(nat_result1.get_remainder())
                if nat_result2.is_successful():
                    return Success([point_result.get_match(), nat_result1.get_match(), nat_result2.get_match()],
                                   nat_result2.get_remainder())

        return Failure("rect <POINT> <NAT> <NAT>", cli_input)

    def has_parameters(self):
        return True


class CircleParser(ShapeCommandParser):
    """
    Parser for "circle" (Circle) Command.
    Definition: ( circle <POINT> <POINT> | circle <POINT> <NAT>) ) <COLOR>
    COLOR := rgb([0,255],[0,255],[0,255]) | <empty string>
    """
    def parse_params(self, cli_input: str) -> ParseResult:
        points_result = self.parse_two_points(cli_input)
        if points_result.is_successful():
            abs_points = self.convert_points(points_result.get_match())
            start_x = abs_points[0].x
            start_y = abs_points[0].y
            end_x = abs_points[1].x
            end_y = abs_points[1].y

            "Parse color"
            color_result = self.parse_color(points_result.get_remainder(), self.color_parser)
            if color_result.is_successful():
                color = color_result.get_match()
                return Success(PrintCircleCommand(self._controller, start_x, start_y, color, end_x=end_x, end_y=end_y), '')
            else:
                return Failure(color_result.get_expected(), points_result.get_remainder())

        point_and_nat_result = self.parse_point_and_nat(cli_input)
        if point_and_nat_result.is_successful():
            radius = point_and_nat_result.get_match()[1]

            abs_point = self.convert_points([point_and_nat_result.get_match()[0]])
            start_x = abs_point[0].x
            start_y = abs_point[0].y

            # Parse color
            color_result = self.parse_color(point_and_nat_result.get_remainder(), self.color_parser)
            if color_result.is_successful():
                color = color_result.get_match()
                return Success(PrintCircleCommand(self._controller, start_x, start_y, color,
                                                  DimensionsCircleFactory, radius=radius), '')
            else:
                return Failure(color_result.get_expected(), point_and_nat_result.get_remainder())

        return Failure(points_result.get_expected() + ' | ' + point_and_nat_result.get_expected(), cli_input)

    def parse_point_and_nat(self, cli_input: str) -> ParseResult:
        """
        Parse a Point and a Natural number from given input.
        """
        nat_parser = NatParser()

        point_result = PointParser().parse_point(cli_input)
        if point_result.is_successful():
            nat_result = nat_parser.parse_input(point_result.get_remainder())
            if nat_result.is_successful():
                return Success([point_result.get_match(), nat_result.get_match()], nat_result.get_remainder())

        return Failure("circle <POINT> <NAT>", cli_input)

    def has_parameters(self) -> bool:
        return True


class DotParser(ShapeCommandParser):
    """
    Parser for "dot" (Dot) Command.
    Definition: dot <POINT> <COLOR>
    COLOR := rgb([0,255],[0,255],[0,255]) | <empty string>
    """
    def parse_params(self, cli_input: str) -> ParseResult:
        point_result = PointParser().parse_point(cli_input)
        if point_result.is_successful():
            abs_point = self.convert_points([point_result.get_match()])
            point_x = abs_point[0].x
            point_y = abs_point[0].y

            # Parse color
            color_result = self.parse_color(point_result.get_remainder(), self.color_parser)
            if color_result.is_successful():
                color = color_result.get_match()
                return Success(PrintDotCommand(self._controller, point_x, point_y, color), '')
            else:
                return Failure(color_result.get_expected(), point_result.get_remainder())

        return Failure("dot <POINT>", cli_input)

    def has_parameters(self) -> bool:
        return True


class LineParser(ShapeCommandParser):
    """
    Parser for "line" (Line) Command.
    If More than two points are parsed as parameters, the result command
    is PolylineCommand instead of LineCommand.
    Definition: line <POINT> <POINTS> <COLOR>
    POINTS ::= <POINT> | <POINT> <POINTS>
    COLOR := rgb([0,255],[0,255],[0,255]) | <empty string>
    """
    def parse_params(self, cli_input: str) -> ParseResult:
        points_result = self.parse_two_points(cli_input)
        if points_result.is_successful():
            points = points_result.get_match()

            # two points parsed successfully, try to parse a color
            remainder = points_result.get_remainder()
            color_result = self.parse_color(remainder, self.color_parser)
            if color_result.is_successful():
                # color parsed successfully, no more points will be parsed
                color = color_result.get_match()

                abs_points = self.convert_points(points_result.get_match())
                start_x = abs_points[0].x
                start_y = abs_points[0].y
                end_x = abs_points[1].x
                end_y = abs_points[1].y
                return Success(PrintLineCommand(self._controller, start_x, start_y, end_x, end_y, color), '')
            else:
                # try to parse a point or a color
                while True:
                    point_result = PointParser().parse_point(remainder)
                    if point_result.is_successful():
                        points.append(point_result.get_match())
                        remainder = point_result.get_remainder()
                    else:
                        color_result = self.parse_color(remainder, self.color_parser)
                        if color_result.is_successful():
                            # color parsed successfully, no more points will be parsed
                            color = color_result.get_match()

                            abs_points = self.convert_points(points)
                            return Success(PrintPolylineCommand(self._controller,
                                                                [(p.x, p.y) for p in abs_points], color),
                                           color_result.get_remainder())
                        else:
                            break

        return Failure("line <POINT> <POINTS>", cli_input)

    def has_parameters(self) -> bool:
        return True

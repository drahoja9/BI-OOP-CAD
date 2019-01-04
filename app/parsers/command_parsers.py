import abc
from builtins import NotImplementedError

from app.parsers.parse_results import ParseResult, Success, Failure
from app.parsers.low_level_parsers import NatParser
from app.parsers.point_parsers import PointParser, AbsoluteParserPoint
from app.parsers.color_parser import ColorParser
from app.shape_factory import DimensionsRectFactory, DimensionsCircleFactory
from app.commands import PrintDotCommand, PrintRectCommand, PrintCircleCommand, PrintLineCommand, \
    PrintPolylineCommand, MoveShapeCommand, RemoveShapeCommand, ListShapeCommand, LoadCommand, SaveCommand, \
    ClearCommand, QuitCommand, Command
from app.utils import Color
from app.controller import Controller


class CommandParser:
    """
    Parses command from CLI input.
    If Command (and it's parameters, if there are any required) is successfully parsed,
    Success(Command, string) is returned.
    """
    def __init__(self, controller: Controller):
        self._controller = controller
        self._command = None

    def get_command(self) -> ParseResult:
        """
        Return a Command instance if it does not require parameters.
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
    def __init__(self, controller: Controller, color_parser: ColorParser):
        super().__init__(controller)
        self.color_parser = color_parser

    def get_command(self) -> ParseResult:
        raise NotImplementedError

    def parse_params(self, cli_input: str) -> ParseResult:
        pass

    def has_parameters(self) -> bool:
        pass

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
    def __init__(self, controller):
        super().__init__(controller)
        self._command = 'move'

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

    def get_command(self):
        pass


class RemoveShapeParser(CommandParser):
    """
    Parser for "remove" (Remove) Command.
    Definition: remove <POINT>
    """
    def __init__(self, controller):
        super().__init__(controller)
        self._command = 'remove'

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

    def get_command(self):
        pass


class ListParser(CommandParser):
    """
    Parser for "ls" (List) Command.
    Definition: ls | ls <POINT>
    """
    def __init__(self, controller):
        super().__init__(controller)
        self._command = 'ls'

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

    def get_command(self):
        pass


class ClearParser(CommandParser):
    """
    Parser for 'clear' (Clear) command.
    """
    def __init__(self, controller):
        super().__init__(controller)
        self._command = 'clear'

    def get_command(self) -> Command:
        return ClearCommand(self._controller)

    def parse_params(self, cli_input: str) -> ParseResult:
        raise NotImplementedError

    def has_parameters(self) -> bool:
        return False


class SaveParser(CommandParser):
    """
    Parser for 'save' (Save) command.
    Definition: save | save <STRING>
    """
    def __init__(self, controller):
        super().__init__(controller)
        self._command = 'save'

    def parse_params(self, cli_input: str) -> ParseResult:
        if cli_input == '':
            return Success(SaveCommand(self._controller), '')
        else:
            return Success(SaveCommand(self._controller, cli_input), '')

    def has_parameters(self) -> bool:
        return True

    def get_command(self) -> Command:
        return SaveCommand(self._controller)


class LoadParser(CommandParser):
    """
    Parser for 'load' (Load) command.
    Definition: load <STRING>
    """
    def __init__(self, controller):
        super().__init__(controller)
        self._command = 'load'

    def parse_params(self, cli_input: str) -> ParseResult:
        if cli_input == '':
            return Success(LoadCommand(self._controller), '')
        else:
            return Success(LoadCommand(self._controller, cli_input), '')

    def has_parameters(self) -> bool:
        return True

    def get_command(self) -> Command:
        return LoadCommand(self._controller)


class QuitParser(CommandParser):
    """
    Parser for 'quit' (Quit) command.
    Definition: quit
    """
    def __init__(self, controller):
        super().__init__(controller)
        self._command = 'quit'

    def get_command(self) -> Command:
        return QuitCommand(self._controller)

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
    def __init__(self, controller, width_parser: NatParser,
                 height_parser: NatParser, color_parser: ColorParser):
        super().__init__(controller, color_parser)
        self._command = 'rect'
        self.width_parser = width_parser
        self.height_parser = height_parser

    def parse_params(self, cli_input: str) -> ParseResult:
        points_result = self.parse_two_points(cli_input)
        if points_result.is_successful():
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
        point_result = PointParser().parse_point(cli_input)
        if point_result.is_successful():
            width_result = self.width_parser.parse_input(point_result.get_remainder())
            if width_result.is_successful():
                height_result = self.height_parser.parse_input(width_result.get_remainder())
                if height_result.is_successful():
                    return Success([point_result.get_match(), width_result.get_match(), height_result.get_match()],
                                   height_result.get_remainder())

        return Failure("rect <POINT> <NAT> <NAT>", cli_input)

    def has_parameters(self):
        return True

    def get_command(self):
        pass


class CircleParser(ShapeCommandParser):
    """
    Parser for "circle" (Circle) Command.
    Definition: ( circle <POINT> <POINT> | circle <POINT> <NAT>) ) <COLOR>
    COLOR := rgb([0,255],[0,255],[0,255]) | <empty string>
    """
    def __init__(self, controller, radius_parser: NatParser, color_parser: ColorParser):
        super().__init__(controller, color_parser)
        self._command = 'circle'
        self.radius_parser = radius_parser

    def parse_params(self, cli_input: str) -> ParseResult:
        points_result = self.parse_two_points(cli_input)
        if points_result.is_successful():
            abs_points = self.convert_points(points_result.get_match())
            start_x = abs_points[0].x
            start_y = abs_points[0].y
            end_x = abs_points[1].x
            end_y = abs_points[1].y

            # Parse color
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
        point_result = PointParser().parse_point(cli_input)
        if point_result.is_successful():
            radius_result = self.radius_parser.parse_input(point_result.get_remainder())
            if radius_result.is_successful():
                return Success([point_result.get_match(), radius_result.get_match()], radius_result.get_remainder())

        return Failure("circle <POINT> <NAT>", cli_input)

    def has_parameters(self) -> bool:
        return True

    def get_command(self):
        pass


class DotParser(ShapeCommandParser):
    """
    Parser for "dot" (Dot) Command.
    Definition: dot <POINT> <COLOR>
    COLOR := rgb([0,255],[0,255],[0,255]) | <empty string>
    """
    def __init__(self, controller, color_parser: ColorParser):
        super().__init__(controller, color_parser)
        self._command = 'dot'

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

    def get_command(self):
        pass


class LineParser(ShapeCommandParser):
    """
    Parser for "line" (Line) Command.
    If More than two points are parsed as parameters, the result command
    is PolylineCommand instead of LineCommand.
    Definition: line <POINT> <POINTS> <COLOR>
    POINTS ::= <POINT> | <POINT> <POINTS>
    COLOR := rgb([0,255],[0,255],[0,255]) | <empty string>
    """
    def __init__(self, controller, color_parser: ColorParser):
        super().__init__(controller, color_parser)
        self._command = 'line'

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

    def get_command(self):
        pass

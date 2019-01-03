from app.parsers.command_parsers import CommandParser, RemoveShapeParser, ListParser, ClearParser, \
    RectParser, CircleParser, DotParser, LineParser, MoveShapeParser, SaveParser, LoadParser, QuitParser
from app.controller import Controller
from app.parsers.color_parser import ColorParser
from app.parsers.low_level_parsers import StringParser, NatParser, IntParser
from app.parsers.point_parsers import PointParser
from app.commands import InvalidCommand


class CliParser:
    """
    Command line input Parser.
    """
    def __init__(self, controller: Controller, color_parser: ColorParser):
        self.controller = controller
        self.color_parser = color_parser
        self.point_parser = PointParser()
        self.int_parser = IntParser()
        self.nat_parser = NatParser()

        # Command Parsers
        self.command_parsers = [
            RemoveShapeParser(controller, "remove"),
            MoveShapeParser(controller, "move"),
            SaveParser(controller, "save"),
            LoadParser(controller, "load"),
            QuitParser(controller, "quit"),
            ListParser(controller, "ls"),
            ClearParser(controller, "clear"),
            RectParser(controller, "rect", self.nat_parser, self.int_parser, self.color_parser),
            CircleParser(controller, "circle", self.nat_parser, self.int_parser, self.color_parser),
            DotParser(controller, "dot", self.nat_parser, self.int_parser, self.color_parser),
            LineParser(controller, "line", self.nat_parser, self.int_parser, self.color_parser)
        ]

    def parse_input(self, cli_input: str):
        """
        Parse given command line input.
        Parse a command using given CommandParsers. If successful, parse
        parameters from the rest of the input.
        :param cli_input: the input from CLI
        :return: corresponding Command if parsing is successful,
        InvalidCommand otherwise
        """
        for parser in self.command_parsers:
            command_result = parser.parse_command(cli_input)
            if command_result.is_successful():
                if parser.has_parameters():
                    return self.parse_params(parser, command_result.get_remainder())
                else:
                    # there must not be any other characters remaining in the input string
                    if command_result.get_remainder() == '':
                        return command_result.get_match()

        return InvalidCommand(self.controller)

    def parse_params(self, command_parser: CommandParser, remainder: str):
        """
        Parse remaining input using given CommandParser into parameters
        if given parser requires any.
        :param command_parser: successfully matched command parser
        :param remainder: the remainder of CLI input to be parsed
        :return: corresponding Command if parsing is successful,
        InvalidCommand otherwise
        """
        params_result = command_parser.parse_params(remainder)
        if params_result.is_successful() and params_result.get_remainder() == '':
            return params_result.get_match()
        else:
            return InvalidCommand(self.controller)

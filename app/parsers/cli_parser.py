from app.parsers.command_parsers import CommandParser, RemoveShapeParser, ListParser, ClearParser, \
    RectParser, CircleParser, DotParser, LineParser, MoveShapeParser, SaveParser, LoadParser, QuitParser
from app.controller import Controller
from app.parsers.color_parser import ColorParser
from app.parsers.low_level_parsers import NatParser, IntParser, WordParser
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
        self.width_parser = NatParser(' ')
        self.height_parser = NatParser()
        self.radius_parser = NatParser()

        self.command_parser = {
            'remove': RemoveShapeParser(controller),
            'move': MoveShapeParser(controller),
            'save': SaveParser(controller),
            'load': LoadParser(controller),
            'quit': QuitParser(controller),
            'ls': ListParser(controller),
            'clear': ClearParser(controller),
            'rect': RectParser(controller, self.width_parser, self.height_parser, self.color_parser),
            'circle': CircleParser(controller, self.radius_parser, self.color_parser),
            'dot': DotParser(controller, self.color_parser),
            'line': LineParser(controller, self.color_parser)
        }

    def parse_input(self, cli_input: str):
        """
        Parse given command line input.
        Parse a command using given CommandParsers. If successful, parse
        parameters from the rest of the input.
        :param cli_input: the input from CLI
        :return: corresponding Command if parsing is successful,
        InvalidCommand otherwise
        """
        # Parsing the first word -> this will be used as a key to the dictionary with respective parsers
        word_parser = WordParser()
        command_result = word_parser.parse_input(cli_input)

        if command_result.is_successful() and command_result.get_match() in self.command_parser:
            parser = self.command_parser[command_result.get_match()]
            if parser.has_parameters():
                return self.parse_params(parser, command_result.get_remainder())
            elif command_result.get_remainder() == '':
                # there must not be any other characters remaining in the input string
                return parser.parse_command(cli_input).get_match()

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

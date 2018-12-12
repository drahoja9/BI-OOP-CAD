from app.parsers.parse_results import *

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

# -------- /TEMPORARY COMMANDS FOR DEBUGGING ------------


class CommandParser:
    """
    Parses command from CLI input.
    If Command (and it's parameters, if there are any required) is successfully parsed,
    Success(Command, string) is returned.
    """
    def __init__(self, string_parser):
        self.string_parser = string_parser

    @abc.abstractmethod
    def parse_command(self, cli_input) -> ParseResult:
        """
        Parse corresponding command from given input.
        """
        return

    @abc.abstractmethod
    def parse_params(self, cli_input) -> ParseResult:
        """
        Parse command's parameters from given input.
        """
        return

    @abc.abstractmethod
    def has_parameters(self) -> bool:
        return


class ListParser(CommandParser):
    """
    Parser for "ls" (list) Command.
    """
    def __init__(self, string_parser):
        super().__init__(string_parser)

    def parse_command(self, cli_input):
        result = self.string_parser.parse_string("ls", cli_input)
        return result

    def parse_params(self, cli_input):
        return Success("Temporary for debugging", "not implemented yet")

    def has_parameters(self):
        return True


class RectParser(CommandParser):
    """
    Parser for "rect" (Rectangle) Command.
    """
    def __init__(self, string_parser, rel_point_parser, abs_point_parser):
        super().__init__(string_parser)
        self.rel_point_parser = rel_point_parser
        self.abs_point_parser = abs_point_parser

    def parse_command(self, cli_input):
        result = self.string_parser.parse_string("rect", cli_input)
        return result

    def parse_params(self, cli_input):
        return Success("Temporary for debugging", "not implemented yet")

    def has_parameters(self):
        return True


class QuitParser(CommandParser):
    """
    Parser for "quit" Command.
    """
    def __init__(self, string_parser):
        super().__init__(string_parser)

    def parse_command(self, cli_input):
        result = self.string_parser.parse_string("quit", cli_input)
        return result

    def parse_params(self, cli_input):
        return NotImplementedError

    def has_parameters(self):
        return False

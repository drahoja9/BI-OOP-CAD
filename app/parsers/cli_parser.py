from app.parsers.command_parsers import *
from app.parsers.point_parsers import *


class CliParser:
    """
    Command line input Parser.
    """
    def parse_input(self, command_parsers, cli_input):
        """
        Parse given command line input.
        Parse a command using given CommandParsers. If successful, parse
        parameters from the rest of the input.
        :param command_parsers: list of CommandParsers
        :param cli_input: the input from CLI
        :return: corresponding Command if parsing is successful,
        InvalidCommand otherwise
        """
        for parser in command_parsers:
            command_result = parser.parse_command(cli_input)
            if command_result.is_successful():
                if parser.has_parameters():
                    return self.parse_params(parser, command_result.get_remainder())
                else:
                    return command_result.get_match()

        return InvalidCommand()

    def parse_params(self, command_parser, remainder):
        """
        Parse remaining input using given CommandParser into parameters
        if given parser requires any.
        :param command_parser: successfully matched command parser
        :param remainder: the remainder of CLI input to be parsed
        :return: corresponding Command if parsing is successful,
        InvalidCommand otherwise
        """
        params_result = command_parser.parse_params(remainder)
        if params_result.is_successful():
            return params_result.get_match()
        else:
            return InvalidCommand()

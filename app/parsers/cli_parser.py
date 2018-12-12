from app.parsers.command_parsers import *
from app.parsers.point_parsers import *


class CliParser:
    """
    Command line input Parser.
    """
    def parse_input(self, command_parsers, cli_input):
        """
        Parse given command line input.
        Parse a command using give CommandParsers. If successful, parse
        parameters from the rest of the input.
        :param command_parsers:
        :param cli_input:
        :return:
        """
        for parser in command_parsers:
            command_result = parser.parse_command(cli_input)
            if command_result.is_successful():
                return self.parse_params(parser, command_result.remainder)

        return InvalidCommand()

    def parse_params(self, command_parser, remainder):
        """
        Parse remaining input using given CommandParser into parameters
        if given parser requires any.
        :param command_parser: sucessfully matched command parser
        :param remainder: the remainder of CLI input to be parsed
        :return: corresponding Command if parsing is successful,
        InvalidCommand otherwise
        """
        if command_parser.has_parameters():
            params_result = command_parser.parse_params(remainder)
            if params_result.is_successful():
                return command_parser.get_command(params_result.expected)  # tady to chce asi nejak vylepsit
            else:
                return InvalidCommand()
        else:
            return command_parser.get_command()

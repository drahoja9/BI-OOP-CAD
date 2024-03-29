import abc

from app.parsers.low_level_parsers import StringParser, NatParser
from app.parsers.parse_results import ParseResult, Success, Failure


class ColorParser:
    @abc.abstractmethod
    def parse_color(self, cli_input: str) -> ParseResult:
        """
        Parse color from input.
        :param cli_input: string
        :return: Success(color definition, remainder) if color was successfully parsed
        from the input, Failure(expected, actual) otherwise
        """
        raise NotImplementedError


class RgbColorParser(ColorParser):
    """
    Parser for color in "rgb([0,255],[0,255],[0,255])" (RGB) format.
    """
    def __init__(self):
        self.first_nat_parser = NatParser(",")
        self.second_nat_parser = NatParser(")")
        self.string_parser = StringParser("rgb", '(')

    def parse_color(self, cli_input: str) -> ParseResult:
        failure = Failure("rgb([0,255],[0,255],[0,255])", cli_input)

        # Parse prefix \"rgb(\"
        prefix_parse_result = self.string_parser.parse_input(cli_input)
        if not prefix_parse_result.is_successful():
            return failure

        # Parse red (first number)
        red_parse_result = self.first_nat_parser.parse_input(prefix_parse_result.get_remainder())
        if not red_parse_result.is_successful():
            return failure

        red = red_parse_result.get_match()

        # Parse green (second number)
        green_parse_result = self.first_nat_parser.parse_input(red_parse_result.get_remainder())
        if not green_parse_result.is_successful():
            return failure

        green = green_parse_result.get_match()

        # Parse blue (third number)
        blue_parse_result = self.second_nat_parser.parse_input(green_parse_result.get_remainder())
        if not blue_parse_result.is_successful():
            return failure

        blue = blue_parse_result.get_match()

        # Check if provided values form valid RGB color
        if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
            return Success((red, green, blue), blue_parse_result.get_remainder())
        else:
            return failure

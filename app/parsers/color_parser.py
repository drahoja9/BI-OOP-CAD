from app.parsers.low_level_parsers import *
from PyQt5.QtGui import QColor


class ColorParser:
    def parse_color(self, cli_input: str, string_parser: StringParser, nat_parser: NatParser) -> ParseResult:
        failure = Failure("rgb(<0,255>,<0,255>,<0,255>)", cli_input)

        "Parse prefix \"rgb(\""
        prefix_parse_result = string_parser.parse_string("rgb", cli_input, "(")
        if not prefix_parse_result.is_successful():
            return failure

        "Parse red (first number)"
        red_parse_result = nat_parser.parse_input(prefix_parse_result.get_remainder(), ",")
        if not red_parse_result.is_successful():
            return failure

        red = red_parse_result.get_match()

        "Parse green (second number)"
        green_parse_result = nat_parser.parse_input(red_parse_result.get_remainder(), ",")
        if not green_parse_result.is_successful():
            return failure

        green = green_parse_result.get_match()

        "Parse blue (third number)"
        blue_parse_result = nat_parser.parse_input(green_parse_result.get_remainder(), ")")
        if not blue_parse_result.is_successful():
            return failure

        blue = blue_parse_result.get_match()

        color = QColor(red, blue, green)
        if color.isValid():
            return Success(color, blue_parse_result.get_remainder())
        else:
            return failure

        """if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
            return Success([red, green, blue], blue_parse_result.get_remainder())
        else:
            return failure"""

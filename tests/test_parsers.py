import pytest
import re

from app.parsers.cli_parser import *
from app.parsers.point_parsers import *
from app.parsers.color_parser import *

from PyQt5.QtGui import QColor

def test_cli_parser():
    cli_parser = CliParser()
    command_parsers = [ListParser(StringParser()),
                       RectParser(StringParser(), PointParser(), NatParser(), IntParser()),
                       QuitParser(StringParser())
                       ]
    command = cli_parser.parse_input(command_parsers, "quit")
    print(command)
    assert isinstance(command, QuitCommand.__class__)


"--------------- Basic types parsers tests ---------------"


def test_string_parser():
    """
    Test StringParser's method "parse_string" used for parsing exact word from the beginning of a given string.
    """

    "Test invalid inputs with space delimiter"
    parser = StringParser()
    invalid_inputs = [('rect', 'recta'), ('rect', 'list rect'), ('rect', 'rect, '), ('rect', 'rect('),
                      ('rect', 'RECT'), ('rect', 'circle'), ('rect', '   circle'),
                      ('rect', 'rect10,20 30,40')]
    for expected, actual in invalid_inputs:
        result = parser.parse_string(expected, actual, ' ')
        assert isinstance(result, Failure)

    "Test valid inputs with space delimiter"
    valid_inputs = [('rect', 'rect +10 -10', '+10 -10'), ('rect', 'rect anything', 'anything'),
                    ('rect', 'rect +1002', '+1002'), ('rect', 'rect +10 12', '+10 12')]
    for expected, actual, remainder in valid_inputs:
        result = parser.parse_string(expected, actual, ' ')
        assert result == Success(expected, remainder)


def test_nat_parser():
    """
    Test NatParser's method "parse_input" used for parsing natural numbers (^\d+(\s+|$)) from a string.
    """
    parser = NatParser()

    "Test invalid inputs with empty  delimiter"
    invalid_inputs = ['+10', '-10', '+1 ', '-1', '+10.5', '10.5', '+ 10', '+-10', '+- 10', '1-0', '10+', '+10+10',
                      'k10', 'k 10', 'k+10', 'k +10', 'k + 10', 'k1k0', '1k0', 'k 10+', 'k1', ' +10',
                      '10k', '10-k', '1k', ' 10', '+10lalala', "", "lala", " ", "  ", "+", '1 0',
                      '10#', '10$', '10^^', '10^4', '10>',  # special characters
                      '10.', '10:', '10-', '1/', '1\\', '10\"', "10\'", '10?', '1!',  # word delimiters
                      '10(', '10)', '10{', '10}', '10[', '10]']  # brackets
    for cli_input in invalid_inputs:
        result = parser.parse_input(cli_input, '')
        assert isinstance(result, Failure)

    "Test invalid inputs with a delimiter"
    invalid_inputs = [('+10_', '.'), ('10_', ','), ('10.$', '$'), ('10 .20', '.'), ('10, 20', ' '),
                      ('  10', ''), ('10', '10')]
    for cli_input, delimiter in invalid_inputs:
        result = parser.parse_input(cli_input, delimiter)
        assert isinstance(result, Failure)

    "Test valid inputs"
    valid_inputs = [('10,+20', ',', 10, '+20'), ('10 some string +10 yes', ' ', 10, 'some string +10 yes'),
                    ('10A delimiterA remainder', 'A delimiter', 10, 'A remainder'),
                    ('10', '', 10, '')]
    for cli_input, delimiter, expected, remainder in valid_inputs:
        result = parser.parse_input(cli_input, delimiter)
        assert result == Success(expected, remainder)


def test_int_parser():
    """
    Test IntParser's method "parse_input" used for parsing integer ([+-]\d+(\s+|$)) from a string.
    """

    "Test invalid inputs with empty delimiter"
    parser = IntParser()
    invalid_inputs = ['10', '+10.5', '10.5', '+ 10', '+-10', '+- 10', '1-0', '10+', '10 +', '+10+10',
                      'k10', 'k 10', 'k+10', 'k +10', 'k + 10', 'k1k0', '1k0', 'k 10+', 'k1', ' +10',
                      '10k', '10 k', '10 +k', '10-k', '1k', ' 10', '+10lalala', "", "lala", " ", "  ", "+", '+1 0',
                      '+10#', '+10$', '+10^^', '+10^4', '+10>',  # special characters
                      '+10.', '+10:', '+10-', '+1/', '+1\\', '+10\"', "+10\'", '+10?', '+1!',  # word delimiters
                      '+10(', '+10)', '+10{', '+10}', '+10[', '+10]']  # brackets
    for cli_input in invalid_inputs:
        result = parser.parse_input(cli_input, '')
        assert isinstance(result, Failure)

    "Test invalid inputs with a delimiter"
    invalid_inputs = [('+10_', '.'), ('-10_', ','), ('-10.$', '$'), ('+10 .-20', '.'), ('-10, -20', ' '),
                      ('  -10', ''), ('-10', '-10')]
    for cli_input, delimiter in invalid_inputs:
        result = parser.parse_input(cli_input, delimiter)
        assert isinstance(result, Failure)

    "Test valid inputs"
    valid_inputs = [('+10,+20', ',', 10, '+20'), ('-1005+200', '+', -1005, '200'),
                    ('-10 some string +10 yes', ' ', -10, 'some string +10 yes'),
                    ('-10A delimiterA remainder', 'A delimiter', -10, 'A remainder')]
    for cli_input, delimiter, expected, remainder in valid_inputs:
        result = parser.parse_input(cli_input, delimiter)
        assert result == Success(expected, remainder)


"--------------- Point parser tests ---------------"


def test_color_parser():
    """
    Test ColorParser's parsing of color in 'rgb(<0,255>,<0,255>,<0,255>)' format.
    """
    parser = ColorParser()

    "Test invalid inputs"
    invalid_inputs = ["rgb( 0,1,2)", " rgb(0,1,2)", "rgb (0,1,2)", "r gb(0,1,2)", "rgb(0, 1,2)",
                      "rgb(0,1, 2)", "rgb(0,1,2 )", "rgb 0,1,2)", "rgb(0,1,2",
                      "rgb(-5,1,2)", "rgb(-5,-1-2)", "rgb(256,1,2)", "rgb(0,256,2)", "rgb(0,1,256)", "rgb(260,300,600)"]
    for cli_input in invalid_inputs:
        result = parser.parse_color(cli_input, StringParser(), NatParser())
        print(result.print())
        assert result == Failure("rgb(<0,255>,<0,255>,<0,255>)", cli_input)

    "Test valid inputs"
    valid_inputs = [("rgb(0,1,2)", QColor(0, 1, 2), ""), ("rgb(255,255,255)", QColor(255, 255, 255), ""),
                    ("rgb(20,30,40) something else", QColor(20, 30, 40), " something else")]
    for cli_input, expected, remainder in valid_inputs:
        result = parser.parse_color(cli_input, StringParser(), NatParser())
        assert result == Success(expected, remainder)


"--------------- Point parser tests ---------------"


def test_point_parser_absolute_points():
    """
    Test PointParser's parsing of absolute points.
    """
    parser = PointParser()

    "Test invalid inputs"
    invalid_inputs = ['10, 20', '10 ,20', '10 , 20', '10 20', '10.20', ' 10,20', '10',
                      '10,', 'x,20', '10,y', 'x,y']
    for cli_input in invalid_inputs:
        result = parser.parse_point(cli_input, NatParser(), IntParser())
        print(result.print())
        assert result == Failure("x,y or (+-)x,(+-)y", cli_input)

    "Test valid inputs"
    valid_inputs = [('10,20', AbsoluteParserPoint(10, 20), ''), ('100,250 something', AbsoluteParserPoint(100, 250), 'something'),
                    ('0,0', AbsoluteParserPoint(0, 0), ''), ('10,20 ', AbsoluteParserPoint(10, 20), ''),
                    ('10,20  ', AbsoluteParserPoint(10, 20), ' '), ('10,20 30,40', AbsoluteParserPoint(10, 20), '30,40')]
    for cli_input, expected, remainder in valid_inputs:
        result = parser.parse_point(cli_input, NatParser(), IntParser())
        assert result == Success(expected, remainder)


def test_point_parser_relative_points():
    """
    Test PointParser's parsing of relative points.
    """
    parser = PointParser()

    "Test invalid inputs"
    invalid_inputs = ['+10, -20', '-10 ,+20', '+10 , -20', '-10 -20', '-10.-20', ' +10,+20', '+10',
                      '-10,', '+x,-20', '-10,+y', '-x,-y']
    for cli_input in invalid_inputs:
        result = parser.parse_point(cli_input, NatParser(), IntParser())
        print(result.print())
        assert result == Failure("x,y or (+-)x,(+-)y", cli_input)

    "Test valid inputs"
    valid_inputs = [('+10,+20', RelativeParserPoint(10, 20), ''), ('+100,-250 something', RelativeParserPoint(100, -250), 'something'),
                    ('-0,+0', RelativeParserPoint(0, 0), ''), ('-10,-20 ', RelativeParserPoint(-10, -20), ''),
                    ('+10,+20  ', RelativeParserPoint(10, 20), ' '), ('+10,-20 -30,-40', RelativeParserPoint(10, -20), '-30,-40'),
                    ('+10,-20 30,40', RelativeParserPoint(10, -20), '30,40')]
    for cli_input, expected, remainder in valid_inputs:
        result = parser.parse_point(cli_input, NatParser(), IntParser())
        assert result == Success(expected, remainder)


"--------------- RelativeParserPoint to AbsoluteParserPoint conversion tests ---------------"


def test_relative_parser_point_conversion():
    points = [(RelativeParserPoint(10, 20), ParserPoint(0, 0), AbsoluteParserPoint(10, 20)),
              (RelativeParserPoint(-10, 10), ParserPoint(10, -10), AbsoluteParserPoint(0, 0)),
              (RelativeParserPoint(10, -10), ParserPoint(-10, 10), AbsoluteParserPoint(0, 0)),
              (RelativeParserPoint(10, 20), ParserPoint(10, 20), AbsoluteParserPoint(20, 40)),
              (RelativeParserPoint(10, 20), ParserPoint(-10, -20), AbsoluteParserPoint(0, 0))]

    for relative_point, predecessor_point, result_point in points:
        assert relative_point.convert_to_absolute(predecessor_point) == result_point


def test_absolute_parser_point_conversion():
    points = [(AbsoluteParserPoint(10, 20), ParserPoint(0, 0), AbsoluteParserPoint(10, 20)),
              (AbsoluteParserPoint(10, 20), ParserPoint(30, 40), AbsoluteParserPoint(10, 20)),
              (AbsoluteParserPoint(10, 20), ParserPoint(-10, -20), AbsoluteParserPoint(10, 20))]

    for absolute_point, predecessor_point, result_point in points:
        assert absolute_point.convert_to_absolute(predecessor_point) == result_point


"--------------- CommandParser tests ---------------"


def test_rect_parser():
    """

    :return:
    """
    cli_parser = CliParser()
    parser = RectParser(StringParser(), PointParser(), NatParser(), IntParser())
    command_parsers = [ListParser(StringParser()),
                       RectParser(StringParser(), PointParser(), NatParser(), IntParser()),
                       QuitParser(StringParser())
                       ]
    command = cli_parser.parse_input(command_parsers, "rect 10,20 30,40")
    print(command)
    command = cli_parser.parse_input(command_parsers, "rect 10,20 30 40")
    print(command)


def test_points_conversion():
    """
    Test Commandarser's conversion of RelativeParserPoints to AbsoluteParserPoints.
    """
    parser = CommandParser(StringParser())

    "Convert only RelativeParserPoints"
    points_before_conversion = [RelativeParserPoint(-10, 20), RelativeParserPoint(10, -20), RelativeParserPoint(-5, -5)]
    points_after_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(0, 0), AbsoluteParserPoint(-5, -5)]

    assert parser.convert_points(points_before_conversion) == points_after_conversion

    "Convert RelativeParserPoints and AbsoluteParserPoints, first point is relative"
    points_before_conversion = [RelativeParserPoint(-10, 20), AbsoluteParserPoint(10, -20), RelativeParserPoint(-5, -5)]
    points_after_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(10, -20), AbsoluteParserPoint(5, -25)]

    assert parser.convert_points(points_before_conversion) == points_after_conversion

    "Convert RelativeParserPoints and AbsoluteParserPoints, first point is absolute"
    points_before_conversion = [AbsoluteParserPoint(-10, 20), RelativeParserPoint(10, -20), RelativeParserPoint(-5, -5)]
    points_after_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(0, 0), AbsoluteParserPoint(-5, -5)]

    assert parser.convert_points(points_before_conversion) == points_after_conversion

    "Convert only AbsoluteParserPoints"
    points_before_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(0, 0), AbsoluteParserPoint(-5, -5)]
    points_after_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(0, 0), AbsoluteParserPoint(-5, -5)]

    assert parser.convert_points(points_before_conversion) == points_after_conversion

    "Empty list conversion"
    try:
        parser.convert_points([])
        assert False
    except AttributeError:
        assert True

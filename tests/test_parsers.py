import pytest

from app.parsers.cli_parser import CliParser
from app.parsers.low_level_parsers import StringParser, NatParser, IntParser
from app.parsers.point_parsers import ParserPoint
from app.parsers.parse_results import Success, Failure
from app.parsers.point_parsers import PointParser, AbsoluteParserPoint, RelativeParserPoint
from app.parsers.color_parser import RgbColorParser
from app.parsers.command_parsers import CommandParser
from app.controller import Controller
from app.commands import PrintDotCommand, PrintRectCommand, PrintCircleCommand, PrintLineCommand, PrintPolylineCommand, \
    RemoveShapeCommand, ListShapeCommand, MoveShapeCommand, ClearCommand, InvalidCommand, SaveCommand, LoadCommand,\
    QuitCommand
from app.shape_factory import DimensionsRectFactory, DimensionsCircleFactory


@pytest.fixture
def controller() -> Controller:
    controller: Controller = "controller"
    return controller


@pytest.fixture
def cli_parser() -> CliParser:
    controller: Controller = "controller"
    return CliParser(controller, RgbColorParser())

# --------------- Low level parsers tests ---------------


def test_string_parser():
    """
    Test StringParser's method "parse_string" used for parsing exact word from the beginning of a given string.
    """

    # Test invalid inputs with space delimiter
    parser = StringParser()
    invalid_inputs = [('rect', 'recta'), ('rect', 'list rect'), ('rect', 'rect, '), ('rect', 'rect('),
                      ('rect', 'RECT'), ('rect', 'circle'), ('rect', '   circle'),
                      ('rect', 'rect10,20 30,40')]
    for expected, actual in invalid_inputs:
        result = parser.parse_string(expected, actual, ' ')
        assert isinstance(result, Failure)

    # Test valid inputs with space delimiter
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

    # Test invalid inputs with empty  delimiter
    invalid_inputs = ['+10', '-10', '+1 ', '-1', '+10.5', '10.5', '+ 10', '+-10', '+- 10', '1-0', '10+', '+10+10',
                      'k10', 'k 10', 'k+10', 'k +10', 'k + 10', 'k1k0', '1k0', 'k 10+', 'k1', ' +10',
                      '10k', '10-k', '1k', ' 10', '+10lalala', "", "lala", " ", "  ", "+", '1 0',
                      '10#', '10$', '10^^', '10^4', '10>',  # special characters
                      '10.', '10:', '10-', '1/', '1\\', '10\"', "10\'", '10?', '1!',  # word delimiters
                      '10(', '10)', '10{', '10}', '10[', '10]']  # brackets
    for cli_input in invalid_inputs:
        result = parser.parse_input(cli_input, '')
        assert isinstance(result, Failure)

    # Test invalid inputs with a delimiter
    invalid_inputs = [('+10_', '.'), ('10_', ','), ('10.$', '$'), ('10 .20', '.'), ('10, 20', ' '),
                      ('  10', ''), ('10', '10')]
    for cli_input, delimiter in invalid_inputs:
        result = parser.parse_input(cli_input, delimiter)
        assert isinstance(result, Failure)

    # Test valid inputs
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

    # Test invalid inputs with empty delimiter
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

    # Test invalid inputs with a delimiter
    invalid_inputs = [('+10_', '.'), ('-10_', ','), ('-10.$', '$'), ('+10 .-20', '.'), ('-10, -20', ' '),
                      ('  -10', ''), ('-10', '-10')]
    for cli_input, delimiter in invalid_inputs:
        result = parser.parse_input(cli_input, delimiter)
        assert isinstance(result, Failure)

    # Test valid inputs
    valid_inputs = [('+10,+20', ',', 10, '+20'), ('-1005+200', '+', -1005, '200'),
                    ('-10 some string +10 yes', ' ', -10, 'some string +10 yes'),
                    ('-10A delimiterA remainder', 'A delimiter', -10, 'A remainder')]
    for cli_input, delimiter, expected, remainder in valid_inputs:
        result = parser.parse_input(cli_input, delimiter)
        assert result == Success(expected, remainder)


# --------------- ColorParsers test ---------------


def test_rgb_color_parser():
    """
    Test RgbColorParser's parsing of color in 'rgb([0,255],[0,255],[0,255])' format.
    """
    parser = RgbColorParser()

    # Test invalid inputs
    invalid_inputs = ["rgb( 0,1,2)", " rgb(0,1,2)", "rgb (0,1,2)", "r gb(0,1,2)", "rgb(0, 1,2)",
                      "rgb(0,1, 2)", "rgb(0,1,2 )", "rgb 0,1,2)", "rgb(0,1,2",
                      "rgb(-5,1,2)", "rgb(-5,-1-2)", "rgb(256,1,2)", "rgb(0,256,2)", "rgb(0,1,256)", "rgb(260,300,600)"]
    for cli_input in invalid_inputs:
        result = parser.parse_color(cli_input)
        assert result == Failure("rgb([0,255],[0,255],[0,255])", cli_input)

    # Test valid inputs
    valid_inputs = [("rgb(0,1,2)", (0, 1, 2), ""), ("rgb(255,255,255)", (255, 255, 255), ""),
                    ("rgb(20,30,40) something else", (20, 30, 40), " something else")]
    for cli_input, expected, remainder in valid_inputs:
        result = parser.parse_color(cli_input)
        assert result == Success(expected, remainder)


# --------------- PointParser tests ---------------


def test_point_parser_absolute_points():
    """
    Test PointParser's parsing of absolute points.
    """
    parser = PointParser()

    # Test invalid inputs
    invalid_inputs = ['10, 20', '10 ,20', '10 , 20', '10 20', '10.20', ' 10,20', '10',
                      '10,', 'x,20', '10,y', 'x,y']
    for cli_input in invalid_inputs:
        result = parser.parse_point(cli_input)
        assert result == Failure("x,y or (+-)x,(+-)y", cli_input)

    # Test valid inputs
    valid_inputs = [('10,20', AbsoluteParserPoint(10, 20), ''),
                    ('100,250 something', AbsoluteParserPoint(100, 250), 'something'),
                    ('0,0', AbsoluteParserPoint(0, 0), ''), ('10,20 ', AbsoluteParserPoint(10, 20), ''),
                    ('10,20  ', AbsoluteParserPoint(10, 20), ' '),
                    ('10,20 30,40', AbsoluteParserPoint(10, 20), '30,40')]
    for cli_input, expected, remainder in valid_inputs:
        result = parser.parse_point(cli_input)
        assert result == Success(expected, remainder)


def test_point_parser_relative_points():
    """
    Test PointParser's parsing of relative points.
    """
    parser = PointParser()

    # Test invalid inputs
    invalid_inputs = ['+10, -20', '-10 ,+20', '+10 , -20', '-10 -20', '-10.-20', ' +10,+20', '+10',
                      '-10,', '+x,-20', '-10,+y', '-x,-y']
    for cli_input in invalid_inputs:
        result = parser.parse_point(cli_input)
        assert result == Failure("x,y or (+-)x,(+-)y", cli_input)

    # Test valid inputs
    valid_inputs = [('+10,+20', RelativeParserPoint(10, 20), ''),
                    ('+100,-250 something', RelativeParserPoint(100, -250), 'something'),
                    ('-0,+0', RelativeParserPoint(0, 0), ''),
                    ('-10,-20 ', RelativeParserPoint(-10, -20), ''),
                    ('+10,+20  ', RelativeParserPoint(10, 20), ' '),
                    ('+10,-20 -30,-40', RelativeParserPoint(10, -20), '-30,-40'),
                    ('+10,-20 30,40', RelativeParserPoint(10, -20), '30,40')]
    for cli_input, expected, remainder in valid_inputs:
        result = parser.parse_point(cli_input)
        assert result == Success(expected, remainder)


# --------------- RelativeParserPoint to AbsoluteParserPoint conversion tests ---------------


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


# --------------- ShapeCommandParsers tests ---------------


def test_circle_parser(controller: Controller, cli_parser: CliParser):
    # Test invalid inputs, two points as parameters
    invalid_inputs = ["circle 10,-20 30,40", "circle 10,20 30,+40", "circle 10,20 30.40", "circle 10 20 30,40",
                      "circle10,20 30,40", " circle 10,20 30,40", "circle 10,20  30,40", "circle 10,20",
                      "circlee 10,20 30,40", "line 10,20 30 ,40", "line 10,20 30, 40", "line 10,20 30 , 40",
                      "circle something",
                      "circle 10,20 30,40 rgb(0,0,-1)", "circle 10,20 30,40 rgb(0,0,0", "circle 10,20 30,40 rgb 0,0,0",
                      "circle 10,20 30,40 rgb(0,1)", "circle 10,20 30,40rgb(0,1,2)", "circle 10,20 30,40   rgb(0,0,0)",
                      "circle 10,20 30,40 rgb(1a,2,3)", "circle 10,20 30,40,rgb(0,2,3)",
                      "circle 10,20 30,40 rgb(256,0,1)", "circle 10,20 30,40 rgb(2, 0,1)",
                      "circle 10,20 30,40 rgb(2.0.1)", "circle 10,20 30,40 rgb(123)"
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs, two points as parameters
    valid_inputs = [("circle 10,20 30,40", PrintCircleCommand(controller, 10, 20, (0, 0, 0), end_x=30, end_y=40)),
                    ("circle 10,20 -10,-20", PrintCircleCommand(controller, 10, 20, (0, 0, 0), end_x=0, end_y=0)),
                    ("circle -5,-5 +5,+5", PrintCircleCommand(controller, -5, -5, (0, 0, 0), end_x=0, end_y=0)),
                    ("circle -5,-5 10,20", PrintCircleCommand(controller, -5, -5, (0, 0, 0), end_x=10, end_y=20)),
                    ("circle 10,20 30,40 rgb(10,20,30)", PrintCircleCommand(controller, 10, 20, (10, 20, 30),
                                                                            end_x=30, end_y=40)),
                    ("circle 10,20 -10,-20 rgb(0,0,0)", PrintCircleCommand(controller, 10, 20, (0, 0, 0),
                                                                           end_x=0, end_y=0))
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected

    # Test invalid inputs, one point and one natural number (radius) as parameters
    invalid_inputs = ["circle 10,20 30 40", "circle 10,20 +30", "circle 10,20 -30", "circle 10,20",
                      "circle10,20 30", " circle 10,20 30", "circle 10,20  30", "circle 10,20   30",
                      "circlee 10,20 30", "circle 10,20 something",
                      "circle 10,20 30 rgb(0,0,-1)", "circle 10,20 30 rgb(0,0,0",
                      "circle 10,20 30 rgb 0,0,0",
                      "circle 10,20 30 rgb(0,1)", "circle 10,20 30rgb(0,1,2)",
                      "circle 10,20 30   rgb(0,0,0)",
                      "circle 10,20 30 rgb(1a,2,3)", "circle 10,20 30,rgb(0,2,3)",
                      "circle 10,20 30 rgb(256,0,1)", "circle 10,20 30 rgb(2, 0,1)",
                      "circle 10,20 30 rgb(2.0.1)", "circle 10,20 30 rgb(123)"
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs, one point and one natural number (radius) as parameters
    valid_inputs = [("circle 10,20 30", PrintCircleCommand(controller, 10, 20, (0, 0, 0),
                                                           DimensionsCircleFactory, radius=30)),
                    ("circle -5,-5 30", PrintCircleCommand(controller, -5, -5, (0, 0, 0),
                                                           DimensionsCircleFactory, radius=30)),
                    ("circle 10,20 30 rgb(10,20,30)", PrintCircleCommand(controller, 10, 20, (10, 20, 30),
                                                                         DimensionsCircleFactory, radius=30)),
                    ("circle 10,20 30 rgb(0,0,0)", PrintCircleCommand(controller, 10, 20, (0, 0, 0),
                                                                      DimensionsCircleFactory, radius=30))
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected


def test_rect_parser(controller: Controller, cli_parser: CliParser):
    """

    :return:
    """
    # Test invalid inputs, two points as parameters
    invalid_inputs = ["rect 10,-20 30,40", "rect 10,20 30,+40", "rect 10,20 30.40", "rect 10 20 30,40",
                      "rect10,20 30,40", " rect 10,20 30,40", "rect 10,20  30,40", "rect 10,20",
                      "rectt 10,20 30,40", "rect something",
                      "rect 10,20 30,40 rgb(0,0,-1)", "rect 10,20 30,40 rgb(0,0,0", "rect 10,20 30,40 rgb 0,0,0",
                      "rect 10,20 30,40 rgb(0,1)", "rect 10,20 30,40rgb(0,1,2)", "rect 10,20 30,40   rgb(0,0,0)",
                      "rect 10,20 30,40 rgb(1a,2,3)", "rect 10,20 30,40,rgb(0,2,3)",
                      "rect 10,20 30,40 rgb(256,0,1)", "rect 10,20 30,40 rgb(2, 0,1)",
                      "rect 10,20 30,40 rgb(2.0.1)", "rect 10,20 30,40 rgb(123)"
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs, two points as parameters
    valid_inputs = [("rect 10,20 30,40", PrintRectCommand(controller, 10, 20, (0, 0, 0), end_x=30, end_y=40)),
                    ("rect 10,20 -10,-20", PrintRectCommand(controller, 10, 20, (0, 0, 0), end_x=0, end_y=0)),
                    ("rect -5,-5 +5,+5", PrintRectCommand(controller, -5, -5, (0, 0, 0), end_x=0, end_y=0)),
                    ("rect -5,-5 10,20", PrintRectCommand(controller, -5, -5, (0, 0, 0), end_x=10, end_y=20)),
                    ("rect 10,20 30,40 rgb(10,20,30)", PrintRectCommand(controller, 10, 20, (10, 20, 30),
                                                                        end_x=30, end_y=40)),
                    ("rect 10,20 -10,-20 rgb(0,0,0)", PrintRectCommand(controller, 10, 20, (0, 0, 0), end_x=0, end_y=0))
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected

    # Test invalid inputs, one point and two natural numbers (width and height) as parameters
    invalid_inputs = ["rect 10,-20 30 40", "rect 10,20 30 +40", "rect 10,20 -30 40", "rect 10 20 30 40",
                      "rect10,20 30 40", " rect 10,20 30 40", "rect 10,20  30 40", "rect 10,20", "rect 10,20 30",
                      "rectt 10,20 30 40", "rect 10,20 something", "rect 10,20 30 something",
                      "rect 10,20 30 ,40", "rect 10,20 30, 40", "rect 10,20 30 , 40",
                      "rect 10,20 30 40 rgb(0,0,-1)", "rect 10,20 30 40 rgb(0,0,0", "rect 10,20 30 40 rgb 0,0,0",
                      "rect 10,20 30 40 rgb(0,1)", "rect 10,20 30 40rgb(0,1,2)", "rect 10,20 30 40   rgb(0,0,0)",
                      "rect 10,20 30 40 rgb(1a,2,3)", "rect 10,20 30 40,rgb(0,2,3)",
                      "rect 10,20 30 40 rgb(256,0,1)", "rect 10,20 30 40 rgb(2, 0,1)",
                      "rect 10,20 30 40 rgb(2.0.1)", "rect 10,20 30 40 rgb(123)"
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs, one point and two natural numbers (width and height) as parameters
    valid_inputs = [("rect 10,20 20 20", PrintRectCommand(controller, 10, 20, (0, 0, 0),
                                                          DimensionsRectFactory, width=20, height=20)),
                    ("rect -10,-20 10 20", PrintRectCommand(controller, -10, -20, (0, 0, 0),
                                                            DimensionsRectFactory, width=10, height=20)),
                    ("rect +10,+20 0 5", PrintRectCommand(controller, 10, 20, (0, 0, 0),
                                                          DimensionsRectFactory, width=0, height=5)),
                    ("rect +10,-20 20 20 rgb(10,20,30)", PrintRectCommand(controller, 10, -20, (10, 20, 30),
                                                                          DimensionsRectFactory, width=20, height=20)),
                    ("rect -10,+20 1000 2 rgb(0,0,0)", PrintRectCommand(controller, -10, 20, (0, 0, 0),
                                                                        DimensionsRectFactory, width=1000, height=2)),
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected


def test_dot_parser(controller: Controller, cli_parser: CliParser):
    """

    :return:
    """
    # Test invalid inputs
    invalid_inputs = ["dot 10,-20", "dot +10,20", "dot 10.20", "dot 10 20",
                      "dot10,20", " dot 10,20", "dot 10,20   ", "dot 10,20 30,40",
                      "dott 10,20", "dot 10 ,20", "dot 10, 20", "dot 10 , 20", "dot something",
                      "dot 10,20 rgb(0,0,-1)", "dot 10,20 30,40 rgb(0,0,0", "dot 10,20 rgb 0,0,0",
                      "dot 10,20 rgb(0,1)", "dot 10,20rgb(0,1,2)", "dot 10,20  rgb(0,0,0)",
                      "dot 10,20 rgb(1a,2,3)", "dot  10,20,rgb(0,2,3)",
                      "dot 10,20 rgb(256,0,1)", "dot 10,20 rgb(2, 0,1)",
                      "dot 10,20 rgb(2.0.1)", "dot 10,20 rgb(123)"
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs
    valid_inputs = [("dot 10,20", PrintDotCommand(controller, 10, 20, (0, 0, 0))),
                    ("dot -10,+20", PrintDotCommand(controller, -10, +20, (0, 0, 0))),
                    ("dot -5,-5", PrintDotCommand(controller, -5, -5, (0, 0, 0))),
                    ("dot 10,20 rgb(10,20,30)", PrintDotCommand(controller, 10, 20, (10, 20, 30))),
                    ("dot -10,-20 rgb(0,0,0)", PrintDotCommand(controller, -10, -20, (0, 0, 0)))
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected


def test_line_parser(controller: Controller, cli_parser: CliParser):
    invalid_inputs = ["line 10,-20 30,40", "line 10,20 30,+40", "line 10,20 30.40", "line 10 20 30,40",
                      "line10,20 30,40", " line 10,20 30,40", "line 10,20  30,40", "line 10,20",
                      "linet 10,20 30,40", "line 10,20 30 ,40", "line 10,20 30, 40", "line 10,20 30 , 40",
                      "line something",
                      "line 10,20 30,40 rgb(0,0,-1)", "line 10,20 30,40 rgb(0,0,0", "line 10,20 30,40 rgb 0,0,0",
                      "line 10,20 30,40 rgb(0,1)", "line 10,20 30,40rgb(0,1,2)", "line 10,20 30,40   rgb(0,0,0)",
                      "line 10,20 30,40 rgb(1a,2,3)", "line 10,20 30,40,rgb(0,2,3)",
                      "line 10,20 30,40 rgb(256,0,1)", "line 10,20 30,40 rgb(2, 0,1)",
                      "line 10,20 30,40 rgb(2.0.1)", "line 10,20 30,40 rgb(123)"
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs, two points
    valid_inputs = [("line 10,20 30,40", PrintLineCommand(controller, 10, 20, 30, 40, (0, 0, 0))),
                    ("line 10,20 -10,-20", PrintLineCommand(controller, 10, 20, 0, 0, (0, 0, 0))),
                    ("line -5,-5 +5,+5", PrintLineCommand(controller, -5, -5, 0, 0, (0, 0, 0))),
                    ("line -5,-5 10,20", PrintLineCommand(controller, -5, -5, 10, 20, (0, 0, 0))),
                    ("line 10,20 30,40 rgb(10,20,30)", PrintLineCommand(controller, 10, 20, 30, 40, (10, 20, 30))),
                    ("line 10,20 -10,-20 rgb(0,0,0)", PrintLineCommand(controller, 10, 20, 0, 0, (0, 0, 0)))
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected

    # Test invalid inputs, three points
    invalid_inputs = ["line 10,20 30,40 50,-60", "line 10,20 30,40 50,+60", "line 10,20 30,40 50.60",
                      "line 10,20 30,40 50 60", "line 10,20 30,40  50,60", "line 10,20 30,40 something",
                      "line 10,20, 30,40 50, 60", "line 10,20, 30,40 50 ,60",
                      "line 10,20 30,40 50,60 rgb(0,0,-1)", "line 10,20 30,40 50,60 rgb(0,0,0",
                      "line 10,20 30,40 rgb 0,0,0", "line 10,20 30,40 50,60 rgb(0,1)",
                      "line 10,20 30,40 50,60  rgb(0,0,0)", "line 10,20 30,40 50,60 rgb(1a,2,3)",
                      "line 10,20 30,40,50,60 rgb(0,2,3)", "line 10,20 30,40 50,60 rgb(256,0,1)",
                      "line 10,20 30,40 50,60 rgb(2, 0,1)", "line 10,20 30,40 50,60 rgb(2.0.1)",
                      "line 10,20 30,40 50,60rgb(0,1,2)", "line 10,20 30,40 50,60 rgb(123)"
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs, three points
    valid_inputs = [("line 10,20 30,40 50,60",
                     PrintPolylineCommand(controller, [(10, 20), (30, 40), (50, 60)], (0, 0, 0))),
                    ("line 10,20 -10,-20 10,20",
                     PrintPolylineCommand(controller, [(10, 20), (0, 0), (10, 20)], (0, 0, 0))),
                    ("line -5,-5 +5,+5 5,5",
                     PrintPolylineCommand(controller, [(-5, -5), (0, 0), (5, 5)], (0, 0, 0))),
                    ("line -5,-5 10,20 -10,-20",
                     PrintPolylineCommand(controller, [(-5, -5), (10, 20), (0, 0)], (0, 0, 0))),
                    ("line 10,20 30,40 50,60 rgb(10,20,30)",
                     PrintPolylineCommand(controller, [(10, 20), (30, 40), (50, 60)], (10, 20, 30))),
                    ("line 10,20 -10,-20 +30,+40 rgb(0,0,0)",
                     PrintPolylineCommand(controller, [(10, 20), (0, 0), (30, 40)], (0, 0, 0))),
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected

    # Test invalid inputs, four points
    invalid_inputs = ["line 10,20 30,40 50,60 70,-80", "line 10,20 30,40 50,60 70,+80",
                      "line 10,20 30,40 50,60 70.80", "line 10,20 30,40 50,60 70 80", "line 10,20 30,40 50,60  70,80",
                      "line 10,20 30,40 50,60 something",
                      "line 10,20, 30,40 50,60 70, 80", "line 10,20, 30,40 50,60 70, 80",
                      "line 10,20 30,40 50,60 70,80 rgb(0,0,-1)", "line 10,20 30,40 50,60 70,80 rgb(0,0,0",
                      "line 10,20 30,40 50,60 70,80 rgb 0,0,0", "line 10,20 30,40 50,60 70,80 rgb(0,1)",
                      "line 10,20 30,40 50,60 70,80  rgb(0,0,0)", "line 10,20 30,40 50,60 70,80 rgb(1a,2,3)",
                      "line 10,20 30,40,50,60 70,80 rgb(0,2,3)", "line 10,20 30,40 50,60 70,80 rgb(256,0,1)",
                      "line 10,20 30,40 50,60 70,80 rgb(2, 0,1)", "line 10,20 30,40 50,60 70,80 rgb(2.0.1)",
                      "line 10,20 30,40 50,60 70,80rgb(0,1,2)", "line 10,20 30,40 50,60 70,80 rgb(123)"
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs, four points
    valid_inputs = [("line 10,20 30,40 50,60 70,80",
                     PrintPolylineCommand(controller, [(10, 20), (30, 40), (50, 60), (70, 80)], (0, 0, 0))),
                    ("line 10,20 -10,-20 10,20 -10,-20",
                     PrintPolylineCommand(controller, [(10, 20), (0, 0), (10, 20), (0, 0)], (0, 0, 0))),
                    ("line -5,-5 +5,+5 5,5 -5,-5",
                     PrintPolylineCommand(controller, [(-5, -5), (0, 0), (5, 5), (0, 0)], (0, 0, 0))),
                    ("line -5,-5 10,20 -10,-20 10,20",
                     PrintPolylineCommand(controller, [(-5, -5), (10, 20), (0, 0), (10, 20)], (0, 0, 0))),
                    ("line 10,20 30,40 50,60 70,80 rgb(10,20,30)",
                     PrintPolylineCommand(controller, [(10, 20), (30, 40), (50, 60), (70, 80)], (10, 20, 30))),
                    ("line 10,20 -10,-20 +30,+40 -30,-40 rgb(0,0,0)",
                     PrintPolylineCommand(controller, [(10, 20), (0, 0), (30, 40), (0, 0)], (0, 0, 0))),
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected


# --------------- Other CommandParsers tests ---------------


def test_move_shape_parser(controller: Controller, cli_parser: CliParser):
    # Test invalid inputs, two points as parameters
    invalid_inputs = ["move 10,-20 30,40", "move 10,20 30,+40", "move 10,20 30.40", "move 10 20 30,40",
                      "move10,20 30,40", " move 10,20 30,40", "move 10,20  30,40", "move 10,20",
                      "movee 10,20 30,40", "move 10,20 30 ,40", "move 10,20 30, 40", "move 10,20 30 , 40",
                      "move something",
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs, two points as parameters
    valid_inputs = [("move 10,20 30,40", MoveShapeCommand(controller, 10, 20, 30, 40)),
                    ("move 10,20 -10,-20", MoveShapeCommand(controller, 10, 20, 0, 0)),
                    ("move -5,-5 +5,+5", MoveShapeCommand(controller, -5, -5, 0, 0)),
                    ("move -5,-5 10,20", MoveShapeCommand(controller, -5, -5, 10, 20))
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected


def test_remove_shape_parser(controller: Controller, cli_parser: CliParser):
    # Test invalid inputs
    invalid_inputs = ["remove 10,-20", "remove +10,20", "remove 10.20", "remove 10 20",
                      "remove10,20", " remove 10,20", "remove 10,20   ", "remove 10,20 30,40",
                      "removet 10,20", "remove 10 ,20", "remove 10, 20", "remove 10 , 20", "remove something",
                      "remove 10,20 something"
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs
    valid_inputs = [("remove 10,20", RemoveShapeCommand(controller, 10, 20)),
                    ("remove -10,+20", RemoveShapeCommand(controller, -10, +20)),
                    ("remove -5,-5", RemoveShapeCommand(controller, -5, -5))
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected


def test_list_shape_parser(controller: Controller, cli_parser: CliParser):
    # Test invalid inputs
    invalid_inputs = ["ls 10,-20", "ls +10,20", "ls 10.20", "ls 10 20",
                      "ls10,20", " ls 10,20", "ls 10,20   ", "ls 10,20 30,40",
                      "lst 10,20", "ls 10 ,20", "ls 10, 20", "ls 10 , 20", "ls 10,20 something",
                      "ls something", "ls  ", " ls",
                      ]
    for cli_input in invalid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == InvalidCommand(controller)

    # Test valid inputs
    valid_inputs = [("ls 10,20", ListShapeCommand(controller, 10, 20)),
                    ("ls -10,+20", ListShapeCommand(controller, -10, +20)),
                    ("ls -5,-5", ListShapeCommand(controller, -5, -5)),
                    ("ls", ListShapeCommand(controller))
                    ]
    for cli_input, expected in valid_inputs:
        command = cli_parser.parse_input(cli_input)
        assert command == expected


def test_clear_parser(controller: Controller, cli_parser: CliParser):
    # Test valid input
    assert cli_parser.parse_input("clear") == ClearCommand(controller)

    # Test invalid input
    assert cli_parser.parse_input(" clear") == InvalidCommand(controller)
    assert cli_parser.parse_input("clear something") == InvalidCommand(controller)
    assert cli_parser.parse_input("clearsomething") == InvalidCommand(controller)


def test_quit_parser(controller: Controller, cli_parser: CliParser):
    # Test valid input
    assert cli_parser.parse_input("quit") == QuitCommand(controller)

    # Test invalid input
    assert cli_parser.parse_input(" quit") == InvalidCommand(controller)
    assert cli_parser.parse_input("quit something") == InvalidCommand(controller)
    assert cli_parser.parse_input("quitsomething") == InvalidCommand(controller)


def test_save_parser(controller: Controller, cli_parser: CliParser):
    # Test valid input
    assert cli_parser.parse_input("save") == SaveCommand(controller)
    assert cli_parser.parse_input("save filename") == SaveCommand(controller, "filename")

    # Test invalid input
    assert cli_parser.parse_input(" save") == InvalidCommand(controller)
    assert cli_parser.parse_input(" save something") == InvalidCommand(controller)
    assert cli_parser.parse_input("savesomething") == InvalidCommand(controller)


def test_load_parser(controller: Controller, cli_parser: CliParser):
    # Test valid input
    assert cli_parser.parse_input("load filename") == LoadCommand(controller, "filename")

    # Test invalid input
    assert cli_parser.parse_input("load") == InvalidCommand(controller)
    assert cli_parser.parse_input(" load") == InvalidCommand(controller)
    assert cli_parser.parse_input(" load something") == InvalidCommand(controller)
    assert cli_parser.parse_input("loadsomething") == InvalidCommand(controller)


def test_points_conversion(controller: Controller):
    """
    Test CommandParser's conversion of RelativeParserPoints to AbsoluteParserPoints.
    """
    parser = CommandParser(controller)

    # Convert only RelativeParserPoints
    points_before_conversion = [RelativeParserPoint(-10, 20), RelativeParserPoint(10, -20), RelativeParserPoint(-5, -5)]
    points_after_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(0, 0), AbsoluteParserPoint(-5, -5)]

    assert parser.convert_points(points_before_conversion) == points_after_conversion

    # Convert RelativeParserPoints and AbsoluteParserPoints, first point is relative
    points_before_conversion = [RelativeParserPoint(-10, 20), AbsoluteParserPoint(10, -20), RelativeParserPoint(-5, -5)]
    points_after_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(10, -20), AbsoluteParserPoint(5, -25)]

    assert parser.convert_points(points_before_conversion) == points_after_conversion

    # Convert RelativeParserPoints and AbsoluteParserPoints, first point is absolute
    points_before_conversion = [AbsoluteParserPoint(-10, 20), RelativeParserPoint(10, -20), RelativeParserPoint(-5, -5)]
    points_after_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(0, 0), AbsoluteParserPoint(-5, -5)]

    assert parser.convert_points(points_before_conversion) == points_after_conversion

    # Convert only AbsoluteParserPoints
    points_before_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(0, 0), AbsoluteParserPoint(-5, -5)]
    points_after_conversion = [AbsoluteParserPoint(-10, 20), AbsoluteParserPoint(0, 0), AbsoluteParserPoint(-5, -5)]

    assert parser.convert_points(points_before_conversion) == points_after_conversion

    # Empty list conversion
    try:
        parser.convert_points([])
        assert False
    except AttributeError:
        assert True

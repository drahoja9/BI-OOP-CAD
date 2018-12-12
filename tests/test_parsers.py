import pytest
import re

from app.parsers.cli_parser import *
from app.parsers.point_parsers import *


"""def test_cli_parser():
    cli_parser = CliParser()
    command_parsers = [ListParser(StringParser()),
                       RectParser(StringParser(), RelPointParser(), AbsPointParser())
                       ]
    command = cli_parser.parse_input(command_parsers, "rect neco")
    print(command)
"""

def test_string_parser():
    """
    Test StringParser's method "parse_string" used for parsing exact word from the beginning of a given string.
    """

    "Test invalid inputs"
    parser = StringParser()
    invalid_inputs = [('rect', 'recta'), ('rect', 'list rect'), ('rect', 'rect, '), ('rect', 'rect('),
                      ('rect', 'RECT'), ('rect', 'circle')]
    for expected, actual in invalid_inputs:
        result = parser.parse_string(expected, actual)
        assert isinstance(result, Failure)

    "Test valid inputs"
    valid_inputs = [('rect', 'rect +10 -10', ['+10', '-10']), ('rect', ' rect anything', ['anything']),
                    ('rect', 'rect     +1002', ['+1002']), ('rect', '   rect  +10     12', ['+10', '12'])]
    for expected, actual, remainder in valid_inputs:
        result = parser.parse_string(expected, actual)
        assert isinstance(result, Success)
        assert result.remainder == remainder


def test_nat_parser():
    """
    Test NatParser's method "parse_nat" used for parsing natural numbers (^\d+(\s+|$)) from a string.
    """

    "Test invalid inputs"
    parser = NatParser()
    invalid_inputs = ['+10', '-10', '+1 ', '-1', '+10.5', '10.5', '+ 10', '+-10', '+- 10', '1-0', '10+', '+10+10',
                      'k10', 'k 10', 'k+10', 'k +10', 'k + 10', 'k1k0', '1k0', 'k 10+', 'k1', ' +10',
                      '10k', '10-k', '1k', ' 10', '+10lalala', "", "lala", " ", "  ", "+",
                      '10#', '10$', '10^^', '10^4', '10>',  # special characters
                      '10.', '10:', '10-', '1/', '1\\', '10\"', "10\'", '10,', '10?', '1!',  # word delimiters
                      '10(', '10)', '10{', '10}', '10[', '10]']  # brackets
    for cli_input in invalid_inputs:
        result = parser.parse_nat(cli_input)
        assert isinstance(result, Failure)

    "Test valid inputs"
    valid_inputs = [('10', 10, ''), ('1', 1, ''), ('41422142', 41422142, ''), ('10 lala', 10, 'lala'),
                    ('10 -1', 10, '-1'), ('10 ', 10, ''), ('10 .', 10, '.'), ('1 +1 -1', 1, '+1 -1')]
    for cli_input, expected, remainder in valid_inputs:
        result = parser.parse_nat(cli_input)
        assert result == Success(expected, remainder)


def test_int_parser():
    """
    Test IntParser's method "parse_integer" used for parsing integer ([+-]\d+(\s+|$)) from a string.
    """

    "Test invalid inputs"
    parser = IntParser()
    invalid_inputs = ['10', '+10.5', '10.5', '+ 10', '+-10', '+- 10', '1-0', '10+', '10 +', '+10+10',
                      'k10', 'k 10', 'k+10', 'k +10', 'k + 10', 'k1k0', '1k0', 'k 10+', 'k1', ' +10',
                      '10k', '10 k', '10 +k', '10-k', '1k', ' 10', '+10lalala', "", "lala", " ", "  ", "+",
                      '+10#', '+10$', '+10^^', '+10^4', '+10>',  # special characters
                      '+10.', '+10:', '+10-', '+1/', '+1\\', '+10\"', "+10\'", '+10,', '+10?', '+1!',  # word delimiters
                      '+10(', '+10)', '+10{', '+10}', '+10[', '+10]']  # brackets
    for cli_input in invalid_inputs:
        result = parser.parse_integer(cli_input)
        assert isinstance(result, Failure)

    "Test valid inputs"
    valid_inputs = [('+10', 10, ''), ('-10', -10, ''), ('+1', 1, ''), ('+41422142', 41422142, ''),
                    ('+10 lala', 10, 'lala'), ('+10 -1', 10, '-1'), ('+10 ', 10, ''), ('+10 .', 10, '.'),
                    ('-1 +1 -1', -1, '+1 -1')]
    for cli_input, expected, remainder in valid_inputs:
        result = parser.parse_integer(cli_input)
        assert result == Success(expected, remainder)


def test_abs_point_parser():
    """

    :return:
    """

    parser = AbsPointParser()
    valid_inputs = [('10,12', '')]
    #parser.parse_input(NatParser, )
    parser = IntParser()
    res = parser.parse_integer('+10')

    assert res == Success(10, '')

import io
import os

import pytest
from PyQt5.QtGui import QColor

from app import Point
from app.printers import Printer, StreamTextPrinter, FileTextPrinter, AbstractTextPrinter
from app.shapes import Dot, Line, Rectangle, Circle


@pytest.fixture
def shapes():
    return [
        Dot(Point(10, 10), QColor('steelblue')),
        Line(Point(1, 1), Point(-1, -1), QColor(1, 1, 1)),
        Rectangle(Point(84, -12), 1, 1, QColor(255, 255, 255)),
        Circle(Point(0, 0), 997, QColor(100, 200, 100))
    ]


def test_abstract_printer():
    empty_printer = Printer()

    with pytest.raises(NotImplementedError):
        empty_printer.print_dot(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_line(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_rectangle(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_circle(None)


def test_abstract_text_printer():
    empty_printer = AbstractTextPrinter()

    with pytest.raises(NotImplementedError):
        empty_printer.print_dot(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_line(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_rectangle(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_circle(None)


def test_stream_printer(shapes):
    stream = io.StringIO()
    text_printer = StreamTextPrinter(stream)

    for shape in shapes:
        shape.print_to(text_printer)

    # The last line is ended also with a `\n`, so the last element after splitting is empty -> that's why we omit it
    lines = stream.getvalue().split('\n')[:-1]
    for idx, line in enumerate(lines):
        assert line == str(shapes[idx])


def test_file_printer(shapes):
    file = 'test_file.txt'
    file_printer = FileTextPrinter(file)

    for shape in shapes:
        shape.print_to(file_printer)

    with open(file, 'r') as f:
        for idx in range(len(shapes)):
            # Last character is always a newline `\n`, so we have to omit that
            assert f.readline()[:-1] == str(shapes[idx])

    os.remove(file)

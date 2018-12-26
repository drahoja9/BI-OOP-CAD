import io
import os
from typing import Dict

import pytest

from app.printers import Printer, StreamTextPrinter, FileTextPrinter, AbstractTextPrinter
from app.shapes_store import Shape


def test_abstract_printer():
    empty_printer = Printer()

    with pytest.raises(NotImplementedError):
        empty_printer.print_dot(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_line(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_polyline(None)

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
        empty_printer.print_polyline(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_rectangle(None)

    with pytest.raises(NotImplementedError):
        empty_printer.print_circle(None)


def test_stream_printer(shapes: Dict[str, Shape]):
    stream = io.StringIO()
    text_printer = StreamTextPrinter(stream)

    for shape in shapes.values():
        shape.print_to(text_printer)

    # The last line is ended also with a `\n`, so the last element after splitting is empty -> that's why we omit it
    lines = stream.getvalue().split('\n')[:-1]
    for idx, line in enumerate(lines):
        key = [*shapes][idx]
        assert line == str(shapes[key])


def test_file_printer(shapes: Dict[str, Shape]):
    file = 'test_file.txt'
    file_printer = FileTextPrinter(file)

    for shape in shapes.values():
        shape.print_to(file_printer)

    with open(file, 'r') as f:
        for idx in range(len(shapes)):
            # Last character is always a newline `\n`, so we have to omit that
            key = [*shapes][idx]
            assert f.readline()[:-1] == str(shapes[key])

    os.remove(file)


def test_canvas_printer(shapes: Dict[str, Shape]):
    ...

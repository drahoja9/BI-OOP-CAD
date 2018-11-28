import pytest

from app.printers import Printer


def test_abstract_printer():
    empty_drawer = Printer()

    with pytest.raises(NotImplementedError):
        empty_drawer.print_dot(None)

    with pytest.raises(NotImplementedError):
        empty_drawer.print_line(None)

    with pytest.raises(NotImplementedError):
        empty_drawer.print_rectangle(None)

    with pytest.raises(NotImplementedError):
        empty_drawer.print_circle(None)

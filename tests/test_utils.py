import pytest
from utils import parse_ports


def test_valid_range():
    assert parse_ports("1-5") == (1, 5)


def test_single_number_rejected():
    with pytest.raises(SystemExit):
        parse_ports("80")


def test_invalid_format():
    with pytest.raises(SystemExit):
        parse_ports("abc")


@pytest.mark.parametrize("bad", [
    "",
    "abc",
    "0-10",
    "1-70000"
])
def test_invalid_ports_rejected(bad):
    with pytest.raises(SystemExit):
        parse_ports(bad)

import pytest
from unittest.mock import patch, MagicMock
from scanner import scan_port, scan_ports


# Test scan_port()

def test_open_port():
    with patch("scanner.socket.socket") as mock_socket:
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0
        mock_socket.return_value.__enter__.return_value = mock_sock

        assert scan_port("127.0.0.1", 80, 1) == 80


def test_closed_port():
    with patch("scanner.socket.socket") as mock_socket:
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 111
        mock_socket.return_value.__enter__.return_value = mock_sock

        assert scan_port("127.0.0.1", 80, 1) is None


# Test scan_ports()

def test_scan_ports():
    with patch("scanner.scan_port") as mock_scan:
        mock_scan.side_effect = [80, None, 443]

        result = scan_ports("127.0.0.1", 80, 82, 1)

        assert result == [80, 443]


def test_no_open_ports():
    with patch("scanner.scan_port") as mock_scan:
        mock_scan.return_value = None

        result = scan_ports("127.0.0.1", 80, 82, 1)

        assert result == []


def test_sorted_open_ports():
    with patch("scanner.scan_port") as mock_scan:
        mock_scan.side_effect = [443, 22, 80]

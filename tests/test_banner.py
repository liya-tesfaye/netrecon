from unittest.mock import patch, MagicMock
from banner import grab_banner


def test_http_server_header():
    with patch("banner.socket.create_connection") as mock_conn:
        mock_sock = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_sock

        mock_sock.recv.return_value = (
            b"HTTP/1.0 200 OK\r\n"
            b"Server: Apache/2.4.58\r\n\r\n"
        )

        result = grab_banner("127.0.0.1", 80)

        assert result == "Apache/2.4.58"


def test_non_http_banner():
    with patch("banner.socket.create_connection") as mock_conn:
        mock_sock = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_sock

        mock_sock.recv.return_value = b"SSH-2.0-OpenSSH_9.2\r\n"

        result = grab_banner("127.0.0.1", 22)

        assert result == "SSH-2.0-OpenSSH_9.2"


def test_empty_response():
    with patch("banner.socket.create_connection") as mock_conn:
        mock_sock = MagicMock()
        mock_conn.return_value.__enter__.return_value = mock_sock

        mock_sock.recv.return_value = b""

        result = grab_banner("127.0.0.1", 80)

        assert result is None


def test_connection_failure():
    with patch("banner.socket.create_connection") as mock_conn:
        mock_conn.side_effect = OSError

        result = grab_banner("127.0.0.1", 80)

        assert result is None

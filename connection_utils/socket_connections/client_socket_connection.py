import socket

from connection_utils.socket_connections import BaseSocketConnection, SafeConnectionMixin


class ClientSocketConnection(SafeConnectionMixin, BaseSocketConnection):
    _server_port: str = None

    @classmethod
    def get_port(cls) -> str:
        if cls._server_port:
            return cls._server_port
        return super().get_port()

    @classmethod
    def create_connection(cls):
        client_socket = socket.socket()  # instantiate
        client_socket.connect(cls.address())  # connect to the server

        return cls(
            conn=client_socket
        )

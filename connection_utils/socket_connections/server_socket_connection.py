import socket

import rsa

from connection_utils.socket_connections import BaseSocketConnection, SafeConnectionMixin


class ServerSocketConnection(SafeConnectionMixin, BaseSocketConnection):
    _limit: int = None
    _listen_port: str = None

    __socket: socket.socket = None

    @classmethod
    def get_port(cls) -> str:
        if cls._listen_port:
            return cls._listen_port
        return super().get_port()

    @classmethod
    def get_limit(cls) -> int:
        return cls._limit

    @classmethod
    def _get_socket(cls):
        if cls.__socket:
            return cls.__socket
        server_socket = socket.socket()  # instantiate
        server_socket.bind(cls.address())
        server_socket.listen(cls.get_limit())

        cls.__socket = server_socket
        return cls.__socket

    @classmethod
    def accept_connection(cls):
        conn, addr = cls._get_socket().accept()
        new_connection = cls(
            conn=conn,
        )
        new_connection.set_sender('server')
        return new_connection, addr

    def get_your_public_key(self):
        return self._temporary_client_public_key

    def send(self, path, client_public_key: rsa.PublicKey, data=None, headers=dict):
        self._temporary_client_public_key = client_public_key
        super(ServerSocketConnection, self).send(path, data, headers)
        self._temporary_client_public_key = None

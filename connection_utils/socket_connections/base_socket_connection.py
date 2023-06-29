import socket

import pickle

from connection_utils.socket_message import SocketMessage


class BaseSocketConnection:
    _host = socket.gethostname()

    @classmethod
    def get_port(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_host(cls) -> str:
        return cls._host

    @classmethod
    def address(cls):
        return cls.get_host(), cls.get_port()

    def __init__(self, conn, bufsize=4096):
        self._bufsize = bufsize
        self._sender = ''
        self._conn = conn
        self.is_closed = False

    def _recieve_decrypted(self, loaded_received_data):
        return SocketMessage.from_socket_data(loaded_received_data)

    def receive(self) -> SocketMessage:
        received_data = self._conn.recv(self._bufsize)
        if not received_data:
            self.close()
            return SocketMessage(path='empty')
        loaded_received_data = pickle.loads(received_data)
        return self._recieve_decrypted(loaded_received_data)

    def _send_encrypted(self, dumped_data):
        self._conn.send(dumped_data)

    def send(self, path, data=None, headers=dict):
        message = SocketMessage(path=path, sender=self._sender)
        message.body = data
        message.headers = headers
        # todo: before send encrypt with server pr key
        dumped_data = pickle.dumps(message.serialize())
        self._send_encrypted(dumped_data)

    def set_sender(self, sender):
        assert sender is not None
        self._sender = sender

    def close(self):
        self.is_closed = True
        self._conn.close()

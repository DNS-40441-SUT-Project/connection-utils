import socket

import pickle

import rsa

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

    def get_recieved_data(self):
        received_data = self._conn.recv(self._bufsize)
        if not received_data:
            self.close()
            return None
        return received_data

    def recieve_decrypted(self, private_key):
        received_data = self.get_recieved_data()
        if not received_data:
            return SocketMessage(path='empty')
        decrypted_message = rsa.decrypt(received_data, private_key)
        return SocketMessage.from_socket_data(pickle.loads(decrypted_message))

    def receive(self) -> SocketMessage:
        received_data = self.get_recieved_data()
        if not received_data:
            return SocketMessage(path='empty')
        return SocketMessage.from_socket_data(pickle.loads(received_data))

    def _send_encrypted(self, dumped_data):
        self._conn.send(dumped_data)

    def get_dumped_message(self, path, data=None, headers=dict):
        message = SocketMessage(path=path, sender=self._sender)
        message.body = data
        message.headers = headers
        return pickle.dumps(message.serialize())

    def send_encrypted(self, path, public_key: rsa.PublicKey, data=None, headers=dict):
        self._conn.send(rsa.encrypt(self.get_dumped_message(path, data, headers), public_key))

    def send(self, path, data=None, headers=dict):
        self._conn.send(self.get_dumped_message(path, data, headers))

    def set_sender(self, sender):
        assert sender is not None
        self._sender = sender

    def close(self):
        self.is_closed = True
        self._conn.close()

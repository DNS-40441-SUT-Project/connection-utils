class SocketMessage:
    def __init__(self, path, sender=''):
        assert path
        self.path = path
        self.sender = sender
        self.headers = dict()
        self.body = None

    def add_header(self, key, value):
        self.headers[key] = value

    def remove_header(self, key):
        del self.headers[key]

    def serialize(self):
        return {
            'path': self.path,
            'sender': self.sender,
            'headers': self.headers,
            'body': self.body,
        }

    def __str__(self):
        return f'{self.sender}: {self.path}\nheaders: {self.headers}\nbody: {self.body}'

    @classmethod
    def from_socket_data(cls, data):
        message = cls(
            path=data['path'],
            sender=data['sender'],
        )
        message.headers = data['headers']
        message.body = data['body']
        return message

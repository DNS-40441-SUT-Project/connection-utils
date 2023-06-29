import rsa


class SafeConnectionMixin:
    my_private_key: rsa.PrivateKey = None
    your_public_key: rsa.PublicKey = None

    def _recieve_decrypted(self, loaded_received_data):
        return super()._recieve_decrypted(rsa.decrypt(loaded_received_data, self.my_private_key))

    def _send_encrypted(self, dumped_data):
        super()._send_encrypted(rsa.encrypt(dumped_data, self.your_public_key))

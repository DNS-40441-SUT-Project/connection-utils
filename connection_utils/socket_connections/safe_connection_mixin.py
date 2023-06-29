import rsa


class SafeConnectionMixin:
    my_private_key: rsa.PrivateKey = None
    your_public_key: rsa.PublicKey = None
    
    def get_my_private_key(self):
        if self.my_private_key is None:
            raise NotImplementedError
        return self.my_private_key
    
    def get_your_public_key(self):
        if self.your_public_key is None:
            raise NotImplementedError
        return self.your_public_key

    def _recieve_decrypted(self, loaded_received_data):
        return super()._recieve_decrypted(rsa.decrypt(loaded_received_data, self.get_my_private_key()))

    def _send_encrypted(self, dumped_data):
        super()._send_encrypted(rsa.encrypt(dumped_data, self.get_your_public_key()))

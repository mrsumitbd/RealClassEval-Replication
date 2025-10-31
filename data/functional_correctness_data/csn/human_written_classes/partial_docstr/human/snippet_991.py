class Credential:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        username_bytes = username.encode('UTF-8')
        password_bytes = password.encode('UTF-8')
        self.length = 2 + len(username_bytes) + len(password_bytes)
        self.bytes = bytearray()
        self.bytes.extend(len(username_bytes).to_bytes(1, byteorder='big'))
        self.bytes.extend(username_bytes)
        self.bytes.extend(len(password_bytes).to_bytes(1, byteorder='big'))
        self.bytes.extend(password_bytes)

    @classmethod
    def from_bytes(cls, data):
        """
        I am so sorry.
        """
        len_username = int.from_bytes(data[0:2], byteorder='big')
        offset_username = 2 + len_username
        username = data[2:offset_username].decode('UTF-8')
        offset_password = 2 + offset_username
        len_password = int.from_bytes(data[offset_username:offset_password], byteorder='big')
        pass_begin = offset_password
        pass_end = offset_password + len_password
        password = data[pass_begin:pass_end].decode('UTF-8')
        return cls(username, password)
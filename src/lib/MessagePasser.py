import struct

class MessagePasser:
    def __init__(self):
        pass

    def receive_message(self, conn):
        """ Receive a length-prefixed message. """
        try:
            length_prefix = conn.recv(4)  # Read the 4-byte length prefix
            if not length_prefix:
                return None
            message_length = struct.unpack("!I", length_prefix)[0]  # Convert to int
            return conn.recv(message_length).decode("utf-8")  # Read exact message length
        except:
            return None

    def send_message(self, conn, message):
        """ Send a message with a length prefix to ensure full reception. """
        encoded_msg = message.encode()
        length_prefix = struct.pack("!I", len(encoded_msg))  # 4-byte unsigned int
        conn.sendall(length_prefix + encoded_msg)  # Send length + message
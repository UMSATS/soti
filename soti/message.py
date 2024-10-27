import datetime
from utils.constants import CmdID, NodeID
from session_logger import parse_msg_body

class Message:
    def __init__(self, msg_bytes: bytes, source: str):
        """Initialize the message from a bytes object."""
        self.bytes = msg_bytes
        # serial parameters
        self.priority = msg_bytes[0]
        self.sender = NodeID(msg_bytes[1])
        self.recipient = NodeID(msg_bytes[2])
        self.cmd_id = CmdID(msg_bytes[3])
        self.body = msg_bytes[4:]
        # additional parameters
        self.time = datetime.datetime.now().strftime("%T")
        self.source = source
        
    def as_dict(self) -> dict:
        """Return the message parameters as a dictionary."""
        return {
            "time": self.time,
            "source": self.source,
            "priority": self.priority,
            "sender-id": self.sender,
            "recipient-id": self.recipient,
            "cmd": self.cmd_id,
            "body": parse_msg_body(self.cmd_id, self.body)
        }
from datetime import datetime
from dataclasses import dataclass, field
from utils.constants import CmdID, NodeID
from session_logger import parse_msg_body

@dataclass
class Message:
    source: str
    priority: int
    sender: NodeID
    recipient: NodeID
    cmd_id: CmdID
    body: bytes = field(default_factory=([0] * 7))
    time: datetime = field(default_factory=
        lambda:datetime.now().strftime("%T")
    )

    @classmethod
    def deserialize(cls, source, msg_bytes: bytes) -> "Message":
        """Create a message from serialized bytes."""
        source = source
        priority = msg_bytes[0]
        sender = NodeID(msg_bytes[1])
        recipient = NodeID(msg_bytes[2])
        cmd_id = CmdID(msg_bytes[3])
        body = msg_bytes[4:]

        return cls(source, priority, sender, recipient, cmd_id, body)

    def serialize(self) -> bytes:
        """Return the serialized bytes of the message."""
        return bytes(bytearray([
            self.priority,
            self.sender.value,
            self.recipient.value,
            self.cmd_id.value])
            + self.body
        )
        
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
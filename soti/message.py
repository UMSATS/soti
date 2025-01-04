from datetime import datetime
from dataclasses import dataclass, field
from utils.constants import DATA_SIZE, CmdID, NodeID
from session_logger import parse_msg_body

@dataclass
class Message:
    # serial parameters
    priority: int
    sender: NodeID
    recipient: NodeID
    cmd_id: CmdID
    body: bytes = field(default_factory=([0] * 7))
    # additional parameters
    source: str = field(default="unspecified")
    time: datetime = field(default_factory=
        lambda: datetime.now().strftime("%T")
    )

    @classmethod
    def deserialize(cls, msg_bytes: bytes) -> "Message":
        """Create a message from serialized bytes."""
        priority = msg_bytes[0]
        sender = NodeID(msg_bytes[1])
        recipient = NodeID(msg_bytes[2])
        cmd_id = CmdID(msg_bytes[3])
        body = msg_bytes[4:]

        return cls(priority, sender, recipient, cmd_id, body)

    def serialize(self) -> bytes:
        """Return the serialized bytes of the message."""
        # Ensure the data field is the correct length.
        data = bytearray(self.body)
        if len(data) > DATA_SIZE:
            return data[:DATA_SIZE]  # Truncate to the specified length
        elif len(data) < DATA_SIZE:
            return data + bytearray(DATA_SIZE - len(data))  # Extend with zeroes

        return bytes(bytearray([
            self.priority,
            self.sender.value,
            self.recipient.value,
            self.cmd_id.value])
            + data
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
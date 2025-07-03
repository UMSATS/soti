from dataclasses import dataclass

from .constants import CmdID, NodeID

# The length of a serialized message in bytes.
MSG_SIZE = 13

# Max size of a message body.
MAX_BODY_SIZE = 7

@dataclass
class Message:
    cmd: CmdID
    body: bytes
    body_size: int
    priority: int
    sender: NodeID
    recipient: NodeID
    is_ack: bool

    @classmethod
    def deserialize(cls, msg_bytes: bytes) -> "Message":
        """Create a message from serialized bytes."""
        body_end_idx = MAX_BODY_SIZE + 1

        cmd = CmdID(msg_bytes[0])
        body = msg_bytes[1:body_end_idx]
        body_size = int(msg_bytes[body_end_idx])
        priority = int(msg_bytes[body_end_idx+1])
        sender = NodeID(msg_bytes[body_end_idx+2])
        recipient = NodeID(msg_bytes[body_end_idx+3])
        is_ack = bool(msg_bytes[body_end_idx+4])

        return cls(cmd, body, body_size, priority, sender, recipient, is_ack)

    def serialize(self) -> bytes:
        """Return the serialized bytes of the message."""
        return bytes([self.cmd.value]) + self.body + bytes([
            self.body_size,
            self.priority,
            self.sender.value,
            self.recipient.value,
            int(self.is_ack)
        ])

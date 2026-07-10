def format_message(msg):
    msg_dict = msg.as_dict()
    
    s = f"[{msg.time}] "

    if msg.is_ack:
        s += f"{msg.recipient.name} ← {msg.sender.name} "
    else:
        s += f"{msg.sender.name} → {msg.recipient.name} "

    s += msg.cmd_id.name + " "
    
    s += str(msg_dict["body"])

    return s
import sys
import json


def loadMessages():
    with open("messages.json", "r") as f:
        messages = json.load(f)
    return messages


def parseMessages(messages):
    commandObjectList = list(filter(
        lambda x: x["acknowledged-command"] == "0x01" and x["reply-data"][0] == "0x45", messages))
    binaryDataList = []
    sortedData = sorted(commandObjectList, key=lambda x: (
        int(x["reply-data"][0], 16) << 8) | int(x["reply-data"][1], 16))
    return sortedData

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from .constants import NodeID, CmdID


DECIMAL_NUMBER_RE = re.compile(r'^-?[0-9\.]+$')


class ValueParser(ABC):
    @abstractmethod
    def validate(self, s: str) -> bool:
        """Checks if the parser can parse the provided string"""

    @abstractmethod
    def parse(self, s: str) -> any:
        """Parses the string into a value"""


class FloatParser(ValueParser):
    def validate(self, s: str) -> bool:
        return DECIMAL_NUMBER_RE.match(s) is not None

    def parse(self, s: str) -> any:
        return float(s)


class IntParser(ValueParser):
    def validate(self, s: str) -> bool:
        return s.isnumeric()
    
    def parse(self, s: str) -> any:
        return int(s)


class HexParser(ValueParser):
    def validate(self, s: str) -> bool:
        if s[0] == '-':
            s = s[1:]
        return s[:2] == "0x"
    
    def parse(self, s: str) -> any:
        if s[0] == '-':
            return -int(s, 16)
        else:
            return int(s, 16)


class BinaryParser(ValueParser):
    def validate(self, s: str) -> bool:
        if s[0] == '-':
            s = s[1:]
        return s[:2] == "0b"
    
    def parse(self, s: str) -> any:
        if s[0] == '-':
            return -int(s, 2)
        else:
            return int(s, 2)


class NodeIDParser(ValueParser):
    def validate(self, s: str) -> bool:
        return s in NodeID.__members__
    
    def parse(self, s: str) -> any:
        return NodeID[s]


class CmdIDParser(ValueParser):
    def validate(self, s: str) -> bool:
        return s in CmdID.__members__
    
    def parse(self, s: str) -> any:
        return CmdID[s]


class BooleanParser(ValueParser):
    def validate(self, s: str) -> bool:
        return s.lower() in ['true', 'false', '0', '1']
    
    def parse(self, s: str) -> any:
        if s.lower() in ['true', '1']:
            return True
        elif s.lower() in ['false', '0']:
            return False
        else:
            raise ValueError(f"Value '{s}' cannot be converted to boolean")


_all_parsers = [
    IntParser(),
    HexParser(),
    BinaryParser(),
    NodeIDParser(),
    CmdIDParser(),
    BooleanParser(),
    FloatParser()
]

_data_type_map = {
    "u8": np.uint8,
    "u16": np.uint16,
    "u32": np.uint32,
    "i8": np.int8,
    "i16": np.int16,
    "i32": np.int32,
    "f32": np.float32
}

_data_validators = {
    "u8": lambda v: is_integer_like(v) and 0 <= get_integer_value(v) < 2**8,
    "u16": lambda v: is_integer_like(v) and 0 <= get_integer_value(v) < 2**16,
    "u32": lambda v: is_integer_like(v) and 0 <= get_integer_value(v) < 2**32,
    "i8": lambda v: is_integer_like(v) and -(2**7) <= get_integer_value(v) < 2**7,
    "i16": lambda v: is_integer_like(v) and -(2**15) <= get_integer_value(v) < 2**15,
    "i32": lambda v: is_integer_like(v) and -(2**31) <= get_integer_value(v) < 2**31,
    "f32": lambda v: isinstance(v, float)
}

def is_integer_like(v: any) -> bool:
    """True if the value is integer-like"""
    return isinstance(v, (int, bool, CmdID, NodeID))

def get_integer_value(v: any) -> int:
    """Returns the value of an integer-like value"""
    if isinstance(v, int):
        return v
    elif isinstance(v, bool):
        return 1 if v else 0
    elif isinstance(v, (CmdID, NodeID)):
        return v.value
    else:
        raise ValueError(f"Value '{v}' has no integer value")


@dataclass
class Value():
    value: any
    data_type: str

    def to_bytes(self) -> bytes:
        try:
            dtype = _data_type_map[self.data_type]
        except KeyError:
            raise ValueError(f"Unkown data type '{self.data_type}'")
        
        raw_bytes = np.dtype(dtype).newbyteorder("<").type(self.value).tobytes()
        
        return raw_bytes

    @staticmethod
    def from_str(s: str, data_type: str | None = None) -> 'Value':
        """
        Extracts the value from the provided string.
        Raises ValueError for invalid values.
        """
        # Remove whitespace
        s = s.strip()

        try:
            value = Value._parse(s, _all_parsers)
        except Exception as e:
            raise ValueError(f"Failed to parse value '{s}': {e}")
        
        if data_type is not None:
            Value._validate_data(value, data_type)

        return Value(value, data_type)

    @staticmethod
    def _parse(s: str, parsers: list[ValueParser]) -> any:
        for p in parsers:
            if p.validate(s):
                return p.parse(s)
        raise ValueError(f"Could not find matching parser for value '{s}'")

    @staticmethod
    def _validate_data(value: any, data_type: str) -> bool:
        """Determines if the value object is valid"""
        try:
            validator = _data_validators[data_type]
        except KeyError:
            raise ValueError(f"Unknown data type 2 '{data_type}'")
        
        return validator(value)

from typing import NamedTuple


class Flags(NamedTuple):
    begin_len: bytes
    end_len: bytes
    file_end: bytes
    fin: bytes

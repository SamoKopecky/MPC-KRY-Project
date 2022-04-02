from typing import NamedTuple


class Flags(NamedTuple):
    HEADER_START: bytes
    HEADER_END: bytes
    DATA_END: bytes
    FIN: bytes



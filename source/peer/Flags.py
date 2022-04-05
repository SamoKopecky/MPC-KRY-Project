from typing import NamedTuple


class Flags(NamedTuple):
    """
    Define a structure to hold the message format flags

    Message format is defined in :doc:`header`
    """
    HEADER_START: bytes
    HEADER_END: bytes
    DATA_END: bytes
    FIN: bytes



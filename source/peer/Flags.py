from typing import NamedTuple


class Flags(NamedTuple):
    """
    Define a structure to hold the message format flags

    Heartbeat flag is used for checking availability

    Message format is defined in :doc:`header`
    """
    HEADER_START: bytes
    HEADER_END: bytes
    DATA_END: bytes
    HEARTBEAT: bytes
    FIN: bytes



class Flags:
    """
    Define a structure to hold the message format flags

    Heartbeat flag is used for checking availability

    Other flags are used for message format that is defined in :doc:`header`
    """

    HEADER_START: bytes = b"HEADER_START"
    HEADER_END: bytes = b"HEADER_END"
    DATA_END: bytes = b"DATA_END"
    FIN: bytes = b"FIN"

    HEARTBEAT: bytes = b"HEARTBEAT"

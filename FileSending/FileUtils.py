# TODO:
# Checks f file exists
# Permission checks

def read_file(file_path) -> bytes:
    file = open(file_path, 'rb')
    return file.read()


def save_file(file_path, file_bytes):
    file = open(file_path, 'wb')
    file.write(file_bytes)

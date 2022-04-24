import ssl
import socket
import os
import threading

from .Flags import Flags
from .utils import init_db
from ..db.Database import Database


class Server(threading.Thread):
    """
    Handle the server side of the peer. It is not a standalone
    server application.
    """

    def __init__(self, port: int, ip: str, name: str, progress_handler, interface_gui_init, passwd: str):
        super().__init__()
        self.stop_loop = threading.Event()
        self.ip = ip
        self.port = port
        self.passwd = passwd
        self.context = ssl.SSLContext
        self.name = name
        self.flags = Flags()
        self.file_location = ""
        self.progress_handler = progress_handler
        self.interface_gui_init = interface_gui_init
        self.secure_socket = socket.socket()
        self.current_conn = socket.socket()
        self.db = None

    def run(self) -> None:
        """
        Listen for new connections and handle them until a stop event is set

        Stop event is set when the main gui window exists to make sure no
        threads are hanging. Handle the newly created connections by
        receiving progress percentages from the receive_body function.
        Also handle heartbeat messages.
        """
        self.db = init_db(self.name, self.passwd)
        try:
            self.init_sock()
        except ssl.SSLError:
            print("Wrong password to private key")
            exit(1)
        while not self.stop_loop.is_set():

            self.start_listening()
            # Check if thread is to be stopped by the main window exiting
            if self.stop_loop.is_set():
                break
            initial_msg = self.current_conn.recv(2048)
            if self.receive_heartbeat(initial_msg):
                continue
            data_len, name, data, end = self.parse_header(initial_msg)
            # call gui init function, wait for button clicked to receive a file -- do this in tinker
            self.interface_gui_init(data_len, name)
            # for loop for handling percentage of file received
            for done_percent in self.receive_body(self.file_location, self.current_conn, data_len, name, data, end):
                self.progress_handler(done_percent)

    def init_sock(self):
        """
        Initialize the `context` that will be by socket binding

        Load certificates, set flags such as if certificates are required
        during the connection creation. Bind to an address and port (socket)
        and wrap it in an SSL context
        """
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        self.context.set_ciphers("AESGCM")
        table = self.db.get_table(Database.app)[0]
        self.context.load_cert_chain(table[3], table[2], password=self.passwd)
        self.context.load_verify_locations(table[1])
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_REQUIRED

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.bind((self.ip, self.port))
        # 5 -- Amount of possible concurrent connection
        sock.listen(5)
        self.secure_socket = self.context.wrap_socket(sock, server_side=True)

    def start_listening(self):
        """
        Accept an incoming connection
        """
        print(f"Listening on: {self.ip, self.port}")
        self.current_conn, addr = self.secure_socket.accept()
        print(f"New connection at: {addr}")

    def receive_heartbeat(self, initial_msg):
        """
        Check if the received data is a heartbeat

        :param bytes initial_msg:
        :return: Was the msg a heartbeat msg
        """
        if initial_msg == self.flags.HEARTBEAT:
            print("Received heartbeat message, sending response")
            self.current_conn.send(self.flags.HEARTBEAT)
            return True
        return False

    def is_data_end(self, raw_data):
        """
        Check if the final sequence of bytes is a DATA_END flag

        DATA_END flag is indicating that the client has sent all the
        data and is going to wait for the FIN flag.

        :param bytes raw_data: File data
        :return: Whether the final sequence is the DATA_END flag
        :rtype: bool
        """
        if raw_data[-len(self.flags.DATA_END):] == self.flags.DATA_END:
            return True
        return False

    def receive_body(self, file_path, conn, file_len, file_name, file_data, data_end):
        """
        Handle actual file data receiving/saving, periodically yield data received %

        Keeps receiving data until a DATA_END flag is detected. Percentages are return
        for each percentage of the data received. Also handle saving the received data
        to a file. When full file has been received send FIN flag to the other peer.

        :param str file_path: Directory path to save the file in
        :param socket.socket conn: Socket the connection was accepted with
        :param int file_len: Receiving file length
        :param bytes file_name: Name of the receiving file
        :param bytes file_data: Data of the receiving file
        :param bool data_end: No more data is being sent
        """
        raw_data = bytes()
        original_len = file_len
        yielded_value = 0
        file = open(f"{file_path}/{file_name.decode('UTF-8')}", 'wb')
        file.write(file_data)
        while not data_end and not self.is_data_end(raw_data):
            try:
                raw_data = conn.recv(4096)
            except (ConnectionResetError, TimeoutError):
                print("Connection error")
                break
            if self.is_data_end(raw_data):
                # Write everything but the DATA_END flag
                file.write(raw_data[:-len(self.flags.DATA_END)])
                break
            file.write(raw_data)
            file_len -= len(raw_data)
            received = 100 - round(file_len / original_len * 100)
            if yielded_value != received and received != 100:
                yielded_value = received
                yield received
        print("Done receiving file, sending FIN")
        yield 100
        file.close()
        conn.send(self.flags.FIN)

    def parse_header(self, data):
        """
        Parse the header, header format defined in :doc:`header`

        :param bytes data: initial received data
        :return: file length, file name, file data
        :rtype: (int, bytes, bytes, bool)
        """
        end = False
        if self.flags.HEADER_START not in data:
            print("Error, wrong header")
            exit(1)
        header_end_index = data.index(self.flags.HEADER_END)
        header = data[len(self.flags.HEADER_START):header_end_index]
        file_data = data[header_end_index + len(self.flags.HEADER_END):]
        if self.is_data_end(file_data):
            end = True
            file_data = file_data[:-len(self.flags.DATA_END)]
        # Decode from binary to decimal
        file_len = int(header[:64], 2)
        file_name = header[64:]
        return file_len, file_name, file_data, end

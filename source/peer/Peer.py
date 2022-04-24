import os
import subprocess
import time

from time import sleep

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from .Client import Client
from .Server import Server


class Peer:
    """
    Connect the server and client together to create the application's peer
    """

    def __init__(self, name: str, port: int, passwd: str, timer_timeout: int = 0):
        # Listen for all connections
        self.server_address = '0.0.0.0'
        self.listen_port = port
        self.name = name
        self.passwd = passwd
        self.retries = 3
        self.timeout = 10
        self.timer_timeout = timer_timeout
        self.encrypted_files = os.path.dirname(os.path.abspath(__file__)) + f'/../../encrypted_files'
        self.server: Server
        self.client = Client(self.name, self.passwd)

    def listen(self, progress_handler, gui_init):
        """
        Create a server object and start the listening thread

        Very simple function which only passes some arguments to the server
        object constructor and starts the listening thread from the outside.

        :param str -> Any progress_handler: handle the information about file sending progress
        :param (int, bytes) -> Any gui_init: initialize GUI when message header is received
        """
        self.server = Server(self.listen_port, self.server_address, self.name, progress_handler, gui_init, self.passwd)
        self.server.start()

    def send_file(self, hostname, port, file_path, gui_update, list_update):
        """
        Connect to the specified socket and send a file contents + header

        Decide if the file should be sent now or in a background process depending
        on the status of the other peer.

        :param str hostname: IP address of the target
        :param int port: port of the target
        :param str file_path: path to the to-be-sent file
        :param () -> None gui_update: Refresh the GUI to update some elements
        :param () -> None list_update: Update list of users in gui
        """
        self.client.db.insert_user(f'{hostname}:{port}')
        list_update()
        if not self.is_alive(hostname, port):
            self.client.available_func(False)
            print("Creating a subprocess for sending a file")
            command = f'{os.path.abspath("app.py")} -bg {hostname} {str(port)} {file_path} {self.name} {self.passwd} {self.timer_timeout}'
            subprocess.Popen(command, shell=True)
            # Stop sending file in this process
            return
        else:
            self.client.available_func(True)
        gui_update()
        self.client.connect(hostname, port)
        file_bytes, file_name = self.file_open_name(file_path)
        self.client.send_file(file_bytes, file_name)

    def is_alive(self, hostname, port):
        """
        Try to send a heartbeat message a specified amount of times

        :param str hostname: IP address of the target
        :param int port: port of the target
        :return: Is the other peer available
        :rtype: bool
        """
        for i in range(self.retries):
            if self.client.send_heartbeat(hostname, port, self.timeout):
                return True
            else:
                print(f"Peer not accessible trying again ({i + 1}/{self.retries})")
                continue
        print("Peer not accessible")
        return False

    def background_send(self, hostname, port, file_path, loop_interval):
        """
        Try to send a file every `loop_interval` amount of seconds

        Save the file data to a temporary encrypted file for the duration
        of waiting.

        :param str hostname: IP address of the target
        :param int port: port of the target
        :param str file_path: File path of the sending file
        :param int loop_interval: Amount of seconds to wait before checking again
        """
        start = int(time.time())
        file_bytes, file_name = self.file_open_name(file_path)

        # Generate key and IV
        aes_key, aes_iv = os.urandom(32), os.urandom(16)
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv), default_backend())

        # Make dir for temp encrypted files
        if not os.path.exists(self.encrypted_files):
            os.mkdir(self.encrypted_files)

        # Encrypt and save
        encrypted_file_path = f'{self.encrypted_files}/{file_name}_{start}'
        encrypted_file = open(encrypted_file_path, 'wb')
        encrypted_file.write(self.aes_encrypt(cipher, file_bytes))
        encrypted_file.close()
        del file_bytes

        # Wait for other peer
        while not self.client.send_heartbeat(hostname, port, self.timeout):
            if int(time.time() - start) >= self.timer_timeout:
                print("timed out, stopping background sending")
                os.remove(encrypted_file_path)
                exit(0)
            sleep(loop_interval)

        # Decrypt and send
        encrypted_file = open(encrypted_file_path, 'rb')
        file_bytes = self.aes_decrypt(cipher, encrypted_file.read())
        encrypted_file.close()
        os.remove(encrypted_file_path)
        self.client.connect(hostname, port)
        self.client.send_file(file_bytes, file_name)
        exit(0)

    @staticmethod
    def file_open_name(file_path):
        """
        Get the file name and read it

        :param str file_path: Path to the file
        :return: file contents and its name
        :rtype: (bytes, str)
        """
        file_name = file_path.split("/")[-1]
        file = open(file_path, 'rb')
        file_bytes = file.read()
        file.close()
        return file_bytes, file_name

    @staticmethod
    def aes_encrypt(cipher, data):
        """
        Encrypt bytes with a given cipher

        :param Cipher cipher: Cipher used for encryption
        :param bytes data: Data to encrypt
        :return:
        """
        encryptor = cipher.encryptor()
        padding = PKCS7(cipher.algorithm.block_size).padder()
        padded_data = padding.update(data) + padding.finalize()
        return encryptor.update(padded_data) + encryptor.finalize()

    @staticmethod
    def aes_decrypt(cipher, data):
        """
        Decrypt bytes with a given cipher

        :param Cipher cipher: Cipher used for decryption
        :param bytes data: Data to decrypt
        :return:
        """
        decryption = cipher.decryptor()
        data = decryption.update(data) + decryption.finalize()
        padding = PKCS7(cipher.algorithm.block_size).unpadder()
        return padding.update(data) + padding.finalize()

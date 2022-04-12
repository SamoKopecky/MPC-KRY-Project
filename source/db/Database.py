from getpass import getpass
from typing_extensions import Self
from unicodedata import name
from sqlcipher3 import dbapi2 as sqlcipher
from playhouse.sqlcipher_ext import *

import os
import socket

# QUESTIOINS
# Co myslime pod pojmom ID? Co by to malo byt?

class Database:

    def __init__(self, hostname):
        self.certs = os.path.dirname(os.path.abspath(__file__)) + '/../certs'
        self.hostname = socket.gethostname()
        self.IP_address = socket.gethostbyname(hostname)
        self.port = socket.socket.getsockname()
        self.id = id
        self.name = name
        self.root_cert = self.certs + '/' + self.name + 'root.crt'
        self.pub_cert = self.certs + '/' + self.name + '-cert.pem'
        self.privkey = self.certs + '/' + self.name + '.key'
    
    def _read_file(file):
        file = open(file, 'r')
        file_content = file.read()
        file.close()

        return file_content

    def connect_database(self):

        database = 'database.db'

        if (os.path.isfile('database.db') == False):
            database = SqlCipherDatabase(None)
            passphrase = getpass('Enter the database password: ')
            database.init('database.db', passphrase=passphrase)
        else:
            conn = sqlcipher.connect(database)
            cursor = conn.cursor()
            cursor.execute('pragma key=%s'),(input('Enter the database password: '))
        
        return conn

    def create_database(conn):
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                    ID TEXT,
                                    hostname TEXT,
                                    IP_address TEXT,
                                    port INTEGER
                                );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS app (
                                    ID TEXT,
                                    root_certificate TEXT,
                                    private_key TEXT,
                                    public_certificate TEXT
                                );""")

    def write_tables(self, conn):
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO users (ID, hostname, IP_address, port)
                            VALUES
                                (?),
                                (?),
                                (?),
                                (?)
                            """), (self.id, self.hostname, self.IP_address, self.port)
        conn.commit()
        
        cursor.execute(""" INSERT IGNORE INTO app (ID, root_certificate, private_key, public_certificate)
                            VALUES
                                (?),
                                (?),
                                (?),
                                (?)
                            """), (self.id, Self._read_file(self.root_cert), Self._read_file(self.pub_cert), Self._read_file(self.privkey))
        conn.commit()

        conn.close()
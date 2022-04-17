from getpass import getpass
from unicodedata import name
from sqlcipher3 import dbapi2 as sqlcipher

import os
import uuid


class Database:

    def __init__(self, user_name, password):
        self.root_folder = os.path.dirname(os.path.abspath(__file__)) + f'{os.sep}..{os.sep}..{os.sep}'
        self.certs = f'{self.root_folder}certs{os.sep}'
        self.dbs = f'{self.root_folder}dbs{os.sep}'
        self.name = user_name
        self.password = password
        self.root_cert = self.certs + 'root.crt'
        self.pub_cert = self.certs + self.name + '-cert.pem'
        self.privkey = self.certs + self.name + '.key'
        self.db = None

    def create_databases(self):
        self.db = sqlcipher.connect(f'{self.dbs}{self.name}-database.db')
        self.db.execute(f'pragma key="{self.password}"')
        self.db.execute("""CREATE TABLE IF NOT EXISTS users (
                                            ID TEXT,
                                            hostname TEXT,
                                            IP_address TEXT,
                                            port INTEGER
                                        );""")

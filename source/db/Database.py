import subprocess
import os

from sqlcipher3 import dbapi2 as sqlcipher


class Database:
    """
    Handle all the operations regarding a database
    """
    id = 0
    users = "users"
    app = "app"

    def __init__(self, user_name: str, password: str):
        self.root_folder = os.path.dirname(os.path.abspath(__file__)) + f'{os.sep}..{os.sep}..{os.sep}'
        self.certs = f'{self.root_folder}certs{os.sep}'
        self.dbs = f'{self.root_folder}dbs{os.sep}'
        self.name = user_name
        self.password = password
        self.root_cert = f'{self.certs}root.crt'
        self.cert = f'{self.certs}{self.name}-cert.pem'
        self.private_key = f'{self.certs}{self.name}.key'
        self.conn = None

    def create_databases(self):
        """
        Create a database for a user, insert certs/key to app table

        Will run a script to create certs/key if not already created.
        Won't override existing certs/key, even if new certs/key were created
        """
        if not os.path.exists(self.dbs):
            os.mkdir(self.dbs)
        db_path = f'{self.dbs}{self.name}-database.db'
        self.conn = sqlcipher.connect(db_path)
        self.conn.execute(f'pragma key="{self.password}"')
        self.create_tables()
        if not os.path.exists(self.cert) or not os.path.exists(self.cert) or not os.path.exists(self.private_key):
            self.create_certs()
            self.insert_app(self.root_cert, self.private_key, self.cert)
            return
        if len(self.get_table(self.app)) == 0:
            self.insert_app(self.root_cert, self.private_key, self.cert)

    def create_tables(self):
        """
        Create table users and app
        """
        self.conn.execute("""CREATE TABLE IF NOT EXISTS users (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_name text,
                                            ip text,
                                            port integer
                                        );""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS app (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            root_cert text,
                                            private_key text,
                                            cert text
                                        );""")

    def insert_user(self, user_name, ip, port):
        """
        Insert a user to the db

        :param str user_name: User name
        :param str ip: IP address
        :param int port: Port
        """
        sql = "INSERT INTO users (user_name, ip, port) VALUES (?, ?, ?)"
        val = (user_name, ip, port)
        self.conn.execute(sql, val)
        self.conn.commit()

    def insert_app(self, root_cert, private_key, cert):
        """
        Insert certs/key paths to the db

        :param str root_cert: Root certificate
        :param str private_key: Users private key
        :param str cert: Users certificate
        """
        print("Inserting to app table")
        sql = "INSERT INTO app (root_cert, private_key, cert) VALUES (?, ?, ?)"
        val = (root_cert, private_key, cert)
        self.conn.execute(sql, val)
        self.conn.commit()

    def get_table(self, table_name):
        """
        Select everything from a table

        :param str table_name:
        """
        sql = f"SELECT * FROM {table_name}"
        return self.conn.execute(sql).fetchall()

    def create_certs(self):
        """
        Create certs/keys using a shell script
        """
        subprocess.run([f'{self.certs}create_keys.sh', self.name, self.password, self.certs])

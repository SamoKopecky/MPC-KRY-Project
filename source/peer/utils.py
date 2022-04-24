import sqlcipher3.dbapi2

from ..db.Database import Database


def init_db(name, passwd):
    db = Database(name, passwd)
    try:
        db.create_databases()
    except sqlcipher3.dbapi2.DatabaseError:
        print("Wrong password to database")
        exit(1)
    return db

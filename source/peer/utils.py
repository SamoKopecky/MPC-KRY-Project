from ..db.Database import Database


def init_db(name, passwd):
    db = Database(name, passwd)
    db.create_databases()
    return db

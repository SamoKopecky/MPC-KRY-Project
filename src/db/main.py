#!/usr/bin/env python3

from sqlcipher3 import dbapi2 as sqlcipher

db = sqlcipher.connect("testing.db")
db.execute('pragma key="testing"')

print(db.execute('select * from people;').fetchall())

import sqlite3

from main import USER_DATABASE

def getConnection():
    return sqlite3.connect(USER_DATABASE)
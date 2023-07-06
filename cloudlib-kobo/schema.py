import connection

def upgrade():
    conn = connection.getConnection()
    table_name="version"
    cursor = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")

    if len(cursor.fetchall()) == 0:
        print("Making version table")
        conn.execute("CREATE TABLE version (version integer PRIMARY KEY);")
        conn.execute("INSERT INTO version VALUES(1);")
        conn.commit()

    version = conn.execute("SELECT version from version;").fetchone()[0]

    if version == 1:
        print("Creating user table")
        conn.execute("CREATE TABLE users (id integer PRIMARY KEY, alias TEXT, login TEXT, password TEXT, url TEXT);")
        conn.execute("UPDATE version set version=2;")
        conn.commit()
        version = 2

    if version == 2:
        print("Up to date")

    conn.close()

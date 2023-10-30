from rpc import post


def getConfig(cookies, url):
    return post(cookies, url, f"/mybooks/current?", "routes/library.$name.mybooks.current")


def save_user(conn, alias, login, password, url):
    conn.execute("INSERT into users (id, alias, login, password, url) VALUES(?, ?, ?, ?, ?)",
                 (None, alias, login, password, url))


def convert(user):
    return {"id": user[0], "alias": user[1], "login": user[2], "password": user[3], "url": user[4]}


def read_all_users(conn):
    cursor = conn.execute("select * from users")
    users = []

    for user in cursor:
        users.append(convert(user))

    return users


def read_user(conn, alias):
    user = conn.execute("select * from users where alias = ?", (alias,)).fetchone()
    return convert(user)

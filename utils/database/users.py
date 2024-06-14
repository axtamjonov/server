import psycopg2


def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dars4",
        user="postgres",
        password="3927"
    )
    conn.autocommit = True
    return conn


def close_db(conn):
    if conn:
        conn.close()


def create_user(fio, chat_id, username):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute(
                f"insert into users (fio, chat_id, username) values ( '{fio}', '{chat_id}', '{username}');",
            )
    close_db(conn)


def update_user(phone, chat_id):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute(
            f"UPDATE users SET phone='{phone}' where chat_id='{chat_id}';"
        )

    close_db(conn)


def delete_user(chat_id):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute(
            f"delete users where chat_id='{chat_id}';"
        )

    close_db(conn)


def get_user_by_id(chat_id):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute(
            f"select * from users where chat_id='{chat_id}';"
        )
        result = cursor.fetchone()
    close_db(conn)
    return result


def get_users():
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute(f"select * from users")
        result = cursor.fetchall()

    close_db(conn)
    return result


def about_me(chat_id):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute(f"select * from users where chat_id='{chat_id}';")
        result = cursor.fetchall()

    close_db(conn)
    return result

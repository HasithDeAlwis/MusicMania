from ..database import connection, CREATE_USER_TABLE, INSERT_USER


DROP_TABLE = "DROP TABLE users"


def test(name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(INSERT_USER, (name,))

    
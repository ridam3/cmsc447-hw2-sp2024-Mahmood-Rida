import sqlite3

def create_connection(db_file):
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Opened database successfully")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created successfully")
    except sqlite3.Error as e:
        print(e)

def insert_user(conn, user):
    """Insert a new user into the users table."""
    sql = ''' INSERT OR IGNORE INTO users(name,id,points)
              VALUES(?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()
        if cur.rowcount == 0:
            print(f"User with ID {user[1]} already exists and was not inserted.")
        else:
            print("Data inserted successfully")
    except sqlite3.Error as e:
        print(e)

def main():
    database = "database.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        name TEXT NOT NULL,
                                        id INTEGER PRIMARY KEY,
                                        points INTEGER
                                    ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_users_table)
    else:
        print("Error!! cannot create the database connection.")

    with conn:
        users = [
            ('Steve Smith', 211, 80),
            ('Lian Wong', 122, 92),
            ('Chris Peterson', 213, 91),
            ('Sai Patel', 524, 94),
            ('Andrew Whitehead', 425, 99),
            ('Lynn Roberts', 626, 90),
            ('Robert Sanders', 287, 75)

        ]
        for user in users:
            insert_user(conn, user)

if __name__ == '__main__':
    main()
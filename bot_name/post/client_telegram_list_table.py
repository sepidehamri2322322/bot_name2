import sqlite3

connection = sqlite3.connect('telegram_bot.db')
cursor = connection.cursor()

# client has a list of telegram channels
create_table_query = """
    CREATE TABLE IF NOT EXISTS client_telegram_list(
        id integer primary key,
        client_id integer,
        chanel_name text,
        chanel_link text,
        score integer,
        status integer,
        created_at date
    );
"""

cursor.execute(create_table_query)
connection.commit()
connection.close()

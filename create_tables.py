import psycopg2
import psycopg2.extras

db = 'dbname=max_jb user=postgres password=Soen@30010010 host=localhost'


connection = psycopg2.connect(db)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

create_users_table = "CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username text, password text)"
cursor.execute(create_users_table)


create_posts_table = "CREATE TABLE IF NOT EXISTS client_posts (id serial PRIMARY KEY, title text, description text)"
cursor.execute(create_posts_table)


connection.commit()
connection.close()

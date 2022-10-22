import os
import psycopg2

conn = psycopg2.connect(
    database=os.environ["DB"],
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"]
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS veggies;")
cur.execute("CREATE TABLE veggies")

import psycopg2
from config import load_config

def get_paginacia(limit, offset):
    config = load_config()
    sql = """select first_name, last_name, phone_number from contacts c join phone_numbers p on c.id = p.contact_id order by id LIMIT %s OFFSET %s"""
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,offset))
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
    l = input("введите limit")
    off = input("введите offset")
    get_paginacia(l,off)
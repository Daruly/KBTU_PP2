import psycopg2
import csv
from config import load_config

def upload_contacts(filename):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(filename, newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        cur.execute("insert into contacts (first_name,last_name) values(%s,%s)", (row[0], row[1]))
                    conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
def upload_phone_numbers(filename):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(filename, newline = '', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        first_name,last_name,phone_number = row

                        cur.execute("select id from contacts where first_name = %s and last_name = %s", (first_name, last_name))
                        contact_id = cur.fetchone()

                        if contact_id:
                            cur.execute("INSERT INTO phone_numbers (contact_id, phone_number) VALUES (%s, %s)", (contact_id[0], phone_number))
                        else:
                            print(f"{first_name} {last_name} не нашелся")
                conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


upload_contacts("contacts.csv")
upload_phone_numbers("phone_numbers.csv")                
import psycopg2
from config import load_config
def name_exist(first_name):
    checking_existence = """SELECT first_name from contacts where first_name = %s""" 
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(checking_existence, (first_name,))
                ans = cur.fetchone()
                if ans == None:
                    return False
                else:
                    return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def updating_data(phone_number,first_name):
    sql = """UPDATE phone_numbers SET phone_number = %s FROM contacts WHERE phone_numbers.contact_id = contacts.id AND contacts.first_name = %s"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (phone_number,first_name))
                conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

first_name = input("введи имя: ")
last_name = input("введи фамилию: ")
phone_number = input("введи номер: ")

if name_exist(first_name):
    updating_data(phone_number,first_name)
else:
    name = """insert into contacts (first_name, last_name) Values (%s,%s) RETURNING id;"""
    phone = """insert into phone_numbers (phone_number,contact_id) Values(%s,%s)"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(name, (first_name,last_name ))
                user_id = cur.fetchone()[0]
                
                cur.execute(phone, (phone_number,user_id ))

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

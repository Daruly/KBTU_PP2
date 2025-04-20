import psycopg2
from config import load_config


def insert_contact():
    #Добавляет контакт и его номер в базу данных
    sql_contacts = """INSERT INTO contacts (first_name, last_name) VALUES (%s, %s) RETURNING id;"""
    sql_phone_numbers = """INSERT INTO phone_numbers (contact_id, phone_number) VALUES (%s, %s);"""

    config = load_config()

    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    phone_number = input("Введите номер телефона: ")

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Вставляем контакт и получаем его id
                cur.execute(sql_contacts, (first_name, last_name))
                contact_id = cur.fetchone()[0]
                
                # Вставляем номер телефона
                cur.execute(sql_phone_numbers, (contact_id, phone_number))

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    

if __name__=='__main__':
    insert_contact()

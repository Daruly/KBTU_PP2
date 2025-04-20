import psycopg2
from config import load_config

def update_contacts():
    update_row_count = 0
    ans = input("Что хотите поменять? (1 - НОМЕР ТЕЛЕФОНА, 2 - ИМЯ, 3 - ФАМИЛИЯ): ")

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if ans == '1':
                    old_phone = input("Введите старый номер телефона: ")
                    new_phone = input("Введите новый номер телефона: ")

                    cur.execute(
                        "UPDATE phone_numbers SET phone_number = %s WHERE phone_number = %s RETURNING contact_id;",
                        (new_phone, old_phone)
                    )

                    update_row_count = cur.rowcount  # Количество обновленных строк

                elif ans == '2':
                    contact_id = input("Введите ID контакта: ")
                    new_first_name = input("Введите новое имя: ")

                    cur.execute(
                        "UPDATE contacts SET first_name = %s WHERE id = %s RETURNING id;",
                        (new_first_name, contact_id)
                    )
                    
                    update_row_count = cur.rowcount  

                elif ans == '3':
                    contact_id = input("Введите ID контакта: ")
                    new_last_name = input("Введите новую фамилию: ")

                    cur.execute(
                        "UPDATE contacts SET last_name = %s WHERE id = %s RETURNING id;",
                        (new_last_name, contact_id)
                    )

                    update_row_count = cur.rowcount  

                conn.commit()

                if update_row_count > 0:
                    print("Обновление прошло")
                else:
                    print("Ничего не изменилось")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    #узнаем если изменилось че то или нет, чекаем в самом postgresql
    return update_row_count

if __name__ == "__main__":
    update_contacts()
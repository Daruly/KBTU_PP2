import psycopg2
from config import load_config

def first_name_and_phone():
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT first_name ||' '|| phone_number as user_name_and_number 
                FROM contacts
                JOIN phone_numbers
                on contacts.id = phone_numbers.contact_id
                order by id""")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def mobile_operator():
    config = load_config()
    check = input("у какого пользователя узнать какой у него оператор? (напишите только его фамилию)").strip()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT phone_number from phone_numbers JOIN contacts on phone_numbers.contact_id = contacts.id WHERE last_name = %s""", (check,))
                ans = cur.fetchall()

                if ans:
                    for result in ans:
                        phone = result[0]  
                        print(f"Найден номер {phone}")  # чекаем
                        if phone.startswith("+7771") or phone.startswith("+7705"):
                            print("beeline")
                        elif phone.startswith("+7707") or phone.startswith("+7747"):
                            print("tele2")
                        elif phone.startswith("+7700") or phone.startswith("+7708"):
                            print("altel")
                        else:
                            print("Оператор не определён")
                else:
                    print("Такой фамилии нет в базе")
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    
def how_many_MB():
    config = load_config()
    pattern_for_beeline = r"^(?:\+7771|\+7705)"  
    pattern_for_tele2 = r"^(?:\+7707|\+7747)"
    pattern_for_altel = r"^(?:\+7700|\+7708)"

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("select count(*) from phone_numbers where phone_number ~ %s", (pattern_for_beeline, ))
                beeline = cur.fetchone()[0]
                print(f"вот столько билайна {beeline}")
                cur.execute("select count(*) from phone_numbers where phone_number ~ %s", (pattern_for_tele2, ))
                tele2 = cur.fetchone()[0]
                print(f"вот столько теле2 {tele2}")
                cur.execute("select count(*) from phone_numbers where phone_number ~ %s", (pattern_for_altel, ))
                altel = cur.fetchone()[0]
                print(f"вот столько алтела {altel}")
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)                

def who_has_this_operator():
    config = load_config()
    pattern_for_beeline = r"^(?:\+7771|\+7705)"  
    pattern_for_tele2 = r"^(?:\+7707|\+7747)"
    pattern_for_altel = r"^(?:\+7700|\+7708)"
    wassup = input("какого оператора хочешь чекнуть? ").strip()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if wassup == 'билайн':
                    cur.execute("select first_name from contacts join phone_numbers on contacts.id = phone_numbers.contact_id where phone_number ~ %s", (pattern_for_beeline,))
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
                if wassup == 'теле2':
                    cur.execute("select first_name from contacts join phone_numbers on contacts.id = phone_numbers.contact_id where phone_number ~ %s", (pattern_for_tele2,))
                    rows1 = cur.fetchall()
                    for row in rows1:
                        print(row)
                if wassup == 'алтел':
                    cur.execute("select first_name from contacts join phone_numbers on contacts.id = phone_numbers.contact_id where phone_number ~ %s", (pattern_for_altel,))
                    rows2 = cur.fetchall()
                    for row in rows2:
                        print(row)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
if __name__ == "__main__":
    first_name_and_phone()
    check = input("хотите ли вы узнать у кого какой оператор связи? Д/Н?").strip()

    print()
    print()
    print()

    if check == "Д":
        mobile_operator()
    else:
        print("эм ну ок")

    print()
    print()
    print()
    permission = input("хотите узнать скок оператор связи в базе данных? Д/Н ").strip()
    if permission == "Д":
        how_many_MB()
    else:
        print("ну почему")
    who_has_this_operator()





                

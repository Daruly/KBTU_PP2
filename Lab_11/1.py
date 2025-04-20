import psycopg2
from config import load_config

def searching_pattern(user_input):
    sql = """
    SELECT * FROM contacts c
    JOIN phone_numbers p ON c.id = p.contact_id
    WHERE c.first_name ILIKE %s OR c.last_name ILIKE %s OR p.phone_number ILIKE %s
    """

    search_terms = user_input.split()

    first_name_pattern = f"%{search_terms[0]}%" 
    phone_number_pattern = f"%{search_terms[1]}%" 
    last_name_pattern = f"%{search_terms[2]}%" 

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name_pattern, last_name_pattern, phone_number_pattern))
                ans = cur.fetchall()
                if ans:
                    for row in ans:
                        print(row)
                else:
                    print("No")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Запрос от пользователя
check = input("введи 3 переменных (Имя номер телефона Фамилия): ").strip()
searching_pattern(check)
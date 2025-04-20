import psycopg2
import json
from config import load_config
def call_forlist(data_list):
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("CALL list_insert(%s::json, %s)", (json.dumps(data_list, ensure_ascii=False),None))
            invalid_phones = cur.fetchone()[0]
    return invalid_phones

data_list = []
while True:
    name = input("Введите имя, (когда захотите остановиться напишите стоп) ")
    if name.lower() == "стоп":
        break
    last_name = input("введите фамилию: ")
    phone = input("введите номер телефона: ")
    data_list.append({"имя": name, "фамилия": last_name, "номер": phone})
invalid_phones = call_forlist(data_list)

if invalid_phones:
    print("У нас тут есть некорректные номера:")
    for phone in invalid_phones:
        print(phone)
else:
    print("все найсс!")
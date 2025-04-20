import psycopg2
from config import load_config





def updating_data(user_name,score,length,level_num):
    sql = """UPDATE user_score  SET score = %s, length = %s, level_num = %s FROM users WHERE user_score.user_id = users.id and user_name = %s"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (score, length,level_num, user_name))
                conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def show_leaders():
    config = load_config()
    ans = []
    showing = """select user_name, score from users join user_score on users.id = user_score.user_id order by score desc limit 3"""
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(showing)
                rows = cur.fetchall()
                for row in rows:
                    ans.append(row)
                return tuple(ans)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def current_data(user_name):
    sql = """select score, length, level_num from user_score join users on users.id = user_score.user_id where user_name = %s"""
    config = load_config()
    try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (user_name, ))
                    res = cur.fetchone()
                    return res if res else (1,1,1)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return (1,1,1)

def user_exist(user_name):
    checking_existence = """SELECT user_name from users where user_name = %s""" 
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(checking_existence, (user_name,))
                ans = cur.fetchone()
                if ans == None:
                    return False
                else:
                    return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)



def insert_user_data(user_name, score,length,level_num):
    users = """INSERT INTO users (user_name) VALUES (%s) RETURNING id;"""
    users_score = """INSERT INTO user_score (user_id, score,length,level_num) VALUES (%s,%s,%s,%s);"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(users, (user_name, ))
                user_id = cur.fetchone()[0]
                
                cur.execute(users_score, (user_id, score,length,level_num))

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
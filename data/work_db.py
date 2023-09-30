import sqlite3
conn = sqlite3.connect('.\data\DataBase.sqlite')
cursor = conn.cursor()

# Упрощаю ввод SQL запросов и при ошибке, выводит введённый запрос
def sql(text: str):
    cursor.execute(text)
    # try:
    #     cursor.execute(text)
    # except Exception as e:
    #     #print(text, '\n', e)
        # return e

# Делает получение инфы легче
def getdata():
    sql(f'SELECT Category FROM Data')
    return cursor.fetchall()

# Преобразует полученные данные в массив для удобства
def get_list_db(list_: list, sort: bool = False):
    new_list = []
    if sort == True:
        list_ = sorted(list_)
    for i in list_:
        for k in i:
            new_list.append(k)
    return new_list

def delete_table(text):
    sql(f"DROP TABLE {text};")
    conn.commit()

def delete_cell(text, column, table):
    sql(f"""DELETE FROM {table}
                WHERE {column} = '{text}'
        """)
    conn.commit()

# Закрывает конект БД
def Close():
    conn.close()

def create_db(name):
    sql(f"""CREATE TABLE {name} (
    Смотрю        TEXT UNIQUE,
    Буду смотреть TEXT UNIQUE,    
    Просмотренные TEXT UNIQUE,
    Любимые       TEXT UNIQUE,
    Брошенные     TEXT UNIQUE);
        """)
    conn.commit()

def insert_data(table, column, text):
    sql(f"""INSERT INTO {table} (
                     {column}
                 )
                 VALUES (
                     '{text}'
                 );
        """)
    conn.commit()

def get_name_table():
    sql("SELECT name FROM sqlite_master")
    names = get_list_db(cursor.fetchall())
    names = [i for i in names if not i.startswith('sqlite') and not i.startswith('Anime')]
    return names

def get_data_from_db(name):
    sql(f"SELECT {name} FROM test")
    return get_list_db(cursor.fetchall())

def get_quantity(name):
    sql(f"SELECT count({name}) FROM test")
    return get_list_db(cursor.fetchall())

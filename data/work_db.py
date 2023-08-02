import sqlite3
conn = sqlite3.connect('.\data\DataBase.db')
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

def delete(text):
    sql(f"DELETE FROM Data WHERE Category = '{text}';")
    conn.commit()

# Закрывает конект БД
def Close():
    conn.close()

def insert_data(name):
    sql(f'INSERT INTO Data(Category) VALUES("{name}")')
    conn.commit()

sql("SELECT name FROM sqlite_master WHERE type='table' AND name='Data'")
table = get_list_db(cursor.fetchall())
if len(table) == 0:
    sql("CREATE TABLE Data (Category TEXT UNIQUE)")
    conn.commit()
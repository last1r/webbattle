import sqlite3

# # создаем соединение с нашей базой данных
# conn = sqlite3.connect('files/database.db')
# cursor = conn.cursor()
#
# # получаем метаданные для таблицы
# # cursor.execute("PRAGMA table_info(item)")
# cursor.execute("SELECT * FROM item")
# database = cursor.fetchall()[0]
# print(database)
#
# # выводим названия полей таблицы
# # fields = cursor.fetchall()
# # for field in fields:
# #     print(field)
# #
# # # закрываем соединение с базой данных
# # conn.close()

# conn1 = sqlite3.connect('files/database.db')
# cursor1 = conn1.cursor()
#
# cursor1.execute("SELECT * FROM item")
#
# database = cursor1.fetchall()
# conn1.close()
#
# conn = sqlite3.connect('instance/rating.db')
# cursor = conn.cursor()
#
# for el in database:
#     if el:
#         cursor.execute(f"UPDATE item SET time = {el[2]}, scores = {round((el[3] * el[4])/el[5], 2)}, fine = {el[4]}, total_scores = {el[5]} WHERE id={el[0]}")
#         print(el[0], round((el[3] * el[4])/el[5], 2), el[3], el[4], el[5])
# conn.commit()
# conn.close()

a = int(input('faeferagargrg:'))
b = 3
print(type(a))
try:
    print(a+b)
except:
    print("An error occurred")
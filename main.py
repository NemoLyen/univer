import mysql.connector

# Функция для выполнения SQL-запроса
def execute_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Функция для подключения к базе данных
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='dbt8', 
            user='root',
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Основная функция
def main():
    # Подключаемся к базе данных
    connection = connect_to_database()

    if not connection:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        # Запрос номера задания
        task_number = int(input("Введите номер задания (1-4): "))

        # Выполнение соответствующего SQL-запроса
        if task_number == 1:
            query = """
                SELECT 
                    RoomID, 
                    Width * Length AS Area, 
                    Width * Length * CeilingHeight AS Volume
                FROM Rooms;
            """
            result = execute_query(connection, query)
            print("Результат запроса:")
            print(result)
        elif task_number == 2:
            query = """
                SELECT 
                    C.CorpsName,
                    COUNT(D.DepartmentID) AS FacultiesCount,
                    GROUP_CONCAT(D.DepartmentName) AS FacultyNames
                FROM Corps C
                LEFT JOIN Rooms R ON C.CorpsID = R.CorpsID
                LEFT JOIN Departments D ON R.DepartmentID = D.DepartmentID
                GROUP BY C.CorpsID;
            """
            result = execute_query(connection, query)
            print("Результат запроса:")
            print(result)
        elif task_number == 3:
            # Добавление нового корпуса
            query = "INSERT INTO Corps (CorpsName) VALUES ('Новый Корпус');"
            execute_query(connection, query)
            print("Корпус добавлен успешно.")

            # Изменение информации о корпусе
            query = "UPDATE Corps SET CorpsName = 'Переименованный Корпус' WHERE CorpsName = 'Новый Корпус';"
            execute_query(connection, query)
            print("Информация о корпусе изменена успешно.")
        elif task_number == 4:
            # Добавление новой комнаты
            query = """
                INSERT INTO Rooms (CorpsID, RoomNumber, LocationInCorps, Width, Length, Purpose, DepartmentID, CeilingHeight) 
                VALUES (1, 104, 'Первый этаж', 8, 10, 'Лекционная', 5, 3);
            """
            execute_query(connection, query)
            print("Комната добавлена успешно.")

            # Изменение назначения комнаты
            query = "UPDATE Rooms SET Purpose = 'Лаборатория' WHERE RoomID = 6;"
            execute_query(connection, query)
            print("Назначение комнаты изменено успешно.")
        else:
            print("Некорректный номер задания. Введите число от 1 до 4.")
    finally:
        # Закрываем соединение с базой данных
        connection.close()

if __name__ == "__main__":
    main()

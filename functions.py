from app import *

def userLogin(login_email, login_password):
    if login_email and login_password:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Sprawdzanie czy istnieje użytkownik
            cursor.execute("SELECT COUNT(1) FROM `Authorization` WHERE `E-Mail` = '" + login_email + "'")
            if cursor.fetchone()[0]:

                # Pobieranie danych
                cursor.execute("SELECT `Password`, `Token`, `Activate` FROM `Authorization` WHERE `E-Mail` = '" + login_email + "'")
                Data = cursor.fetchall()[0]

                print("Tak")
                return True

            else:

                print("Nie")
                return False

        # Error Log
        except Exception as Error:
            print("userLogin - MySQL Error")
            print("Error: " + str(Error))
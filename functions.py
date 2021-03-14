from hashlib import md5

from app import *
from others import *

def getUserID(mail):
    if mail:
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT ID FROM Authorization WHERE Mail = '" + str(mail) + "'")
            ID = cursor.fetchone()
            cursor.close()

            return ID[0]

        except Exception as Error:
            print("getUserID - Error")
            print("Error: " + str(Error))
    else:
        print("getUserID - Missing value")

### LOGOWANIE

def userLogin(login_email, login_password):
    if login_email and login_password:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Sprawdzanie czy istnieje użytkownik
            cursor.execute("SELECT COUNT(1) FROM `Authorization` WHERE `Mail` = '" + login_email + "'")
            if cursor.fetchone()[0]:

                # Pobieranie danych
                cursor.execute("SELECT `Password`, `Token`, `Name`, `Activate` FROM `Authorization` WHERE `Mail` = '" + login_email + "'")
                Data = cursor.fetchall()[0]

                if md5((login_password + Data[1]).encode('utf-8')).hexdigest() == Data[0]:

                    return True

                else:

                    print("Bledne hasło")
                    return False

            else:

                return False

        # Error Log
        except Exception as Error:
            print("userLogin - MySQL Error")
            print("Error: " + str(Error))

def userRegister(register_username, register_email, register_password):
    if register_username and register_email and register_password:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Sprawdzanie czy istnieje użytkownik
            cursor.execute("SELECT COUNT(1) FROM `Authorization` WHERE `Mail` = '" + register_email + "'")
            if not cursor.fetchone()[0]:

                Token = tokenGenerator()

                register_password = md5((register_password + Token).encode('utf-8')).hexdigest()

                # Dodanie do bazy MySQL
                # to_MySQL = (str(register_email), str(register_username), str(register_password), str(Token))
                # cursor.execute("INSERT INTO Authorization (Mail, Name, Password, Token) VALUES (%s, %s, %s, %s)", to_MySQL)
                # connection.commit()

                sendWelcomeMail(str(register_email), str(getUserID(register_email)), str(Token))

                return True

            else:

                print("Podane konto istnieje")
                return False

        # Error Log
        except Exception as Error:
            print("userRegister - MySQL Error")
            print("Error: " + str(Error))

def userActivate(ID, KEY):
    if ID and KEY:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT Token FROM Authorization WHERE ID = '" + str(ID) + "'")
            Token = cursor.fetchone()

            if Token[0] == KEY:

                cursor.execute("UPDATE Authorization SET Activate = '" + str(1) + "' WHERE `ID` = '" + str(ID) + "'")
                connection.commit()

                return True

            else:

                print("Błędny token!")

                return False

            # Rozłączenie z bazą MySQL
            cursor.close()

        # Error Log
        except Exception as Error:
            print("userActivate - MySQL Error")
            print("Error: " + str(Error))

### LOGOWANIE

def getSongsList():
    try:
        # Łączność z MYSQL
        connection = mysql.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT Token FROM Authorization WHERE ID = '" + str(ID) + "'")
        Token = cursor.fetchone()

        if Token[0] == KEY:

            cursor.execute("UPDATE Authorization SET Activate = '" + str(1) + "' WHERE `ID` = '" + str(ID) + "'")
            connection.commit()

            return True

        else:

            print("Błędny token!")

            return False

        # Rozłączenie z bazą MySQL
        cursor.close()

    # Error Log
    except Exception as Error:
        print("userActivate - MySQL Error")
        print("Error: " + str(Error))
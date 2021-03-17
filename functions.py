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

def getUserIDbyToken(token):
    if token:
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT ID FROM Authorization WHERE Token = '" + str(token) + "'")
            ID = cursor.fetchone()
            cursor.close()

            return ID[0]

        except Exception as Error:
            print("getUserIDbyToken - Error")
            print("Error: " + str(Error))
    else:
        print("getUserIDbyToken - Missing value")

def getUsername(mail):
    if mail:
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM Authorization WHERE Mail = '" + str(mail) + "'")
            Name = cursor.fetchone()
            cursor.close()

            # Development
            if Type == "Development":
                print("getUsername: " + Name[0])

            return Name[0]

        except Exception as Error:
            print("getUsername - Error")
            print("Error: " + str(Error))
    else:
        print("getUsername - Missing value")

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

                if md5((login_password + Data[1]).encode('utf-8')).hexdigest() == Data[0] and Data[3] == True:

                    flash("Pomyślnie zalogowano", "success")
                    return True

                else:

                    flash("Wprowadz poprawne hasło lub aktywuj konto", "error")
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
                to_MySQL = (str(register_email), str(register_username), str(register_password), str(Token))
                cursor.execute("INSERT INTO Authorization (Mail, Name, Password, Token) VALUES (%s, %s, %s, %s)", to_MySQL)
                connection.commit()

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

                return False

            # Rozłączenie z bazą MySQL
            cursor.close()

        # Error Log
        except Exception as Error:
            print("userActivate - MySQL Error")
            print("Error: " + str(Error))

### SONGS

def getSongsList():
    try:
        # Łączność z MYSQL
        connection = mysql.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT `ID`, `Name`, `Artist`, `Time`, `File` FROM Songs")
        SongsList = cursor.fetchall()

        # Development
        if Type == "Development":
            print("SongsList: " + str(SongsList))

        return SongsList

        # Rozłączenie z bazą MySQL
        cursor.close()


    # Error Log
    except Exception as Error:
        print("userActivate - MySQL Error")
        print("Error: " + str(Error))

def getSongInfo(ID):
    try:
        # Łączność z MYSQL
        connection = mysql.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT `ID`, `Name`, `Artist`, `Time`, `File` FROM Songs WHERE ID = '" + str(ID) + "'")
        SongInfo = cursor.fetchall()

        # Development
        if Type == "Development":
            print("SongInfo: " + str(SongInfo))

        return SongInfo

        # Rozłączenie z bazą MySQL
        cursor.close()


    # Error Log
    except Exception as Error:
        print("userActivate - MySQL Error")
        print("Error: " + str(Error))

def getFavoritesSongsList(UserID):
    try:
        # Łączność z MYSQL
        connection = mysql.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT Song_ID FROM Favorites WHERE User_ID = '" + str(UserID) + "'")
        SongsList = cursor.fetchall()

        Table = []

        for Data in SongsList:
            Table.append(Data[0])

        # Development
        if Type == "Development":
            print("FavoritesSongsList: " + str(Table))

        return Table

        # Rozłączenie z bazą MySQL
        cursor.close()


    # Error Log
    except Exception as Error:
        print("userActivate - MySQL Error")
        print("Error: " + str(Error))

def addToFavorite(userID, songID):
    if userID and songID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(1) FROM `Favorites` WHERE `User_ID` = '" + str(userID) + "' AND `Song_ID` = '" + str(songID) + "'")
            if not cursor.fetchone()[0]:

                # Dodanie do bazy MySQL
                to_MySQL = (str(userID), str(songID))
                cursor.execute("INSERT INTO Favorites (User_ID, Song_ID) VALUES (%s, %s)", to_MySQL)
                connection.commit()

                # Development
                if Type == "Development":
                    print("FavoritesSongs Add (" + str(userID) + "): " + str(songID))

            else:

                # Usuwanie
                cursor.execute("DELETE FROM Favorites WHERE  User_ID = '" + str(userID) + "' AND  Song_ID = '" + str(songID) + "'")
                connection.commit()

                # Development
                if Type == "Development":
                    print("FavoritesSongs Remove (" + str(userID) + "): " + str(songID))

            return True

            # Rozłączenie z bazą MySQL
            cursor.close()

        # Error Log
        except Exception as Error:
            print("addToFavorite - MySQL Error")
            print("Error: " + str(Error))

### OTHERS

def sendWelcomeMail(recipient, id, token):
    msg = Message('AmbiWave', sender='ambiwaveapp@gmail.com', recipients=[recipient])
    msg.html = "Kod aktywacyjny: http://evgaming.duckdns.org:70/activate/"+ id +"/" + token
    mail.send(msg)
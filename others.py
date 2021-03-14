from app import *

import random
import re
import string

from flask_mail import Message

def sendWelcomeMail(recipient, id, token):
    msg = Message('AmbiWave', sender='kamyrdol32test@gmail.com', recipients=[recipient])
    msg.html = "Kod aktywacyjny: http://evgaming.duckdns.org:70/activate/" + id +"/" + token
    mail.send(msg)

def tokenGenerator(stringlength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringlength))

Regex_Mail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(Type, Object):
    print(Type + " " + Object)
    if Type == "Mail":
        if re.search(Regex_Mail, Object) or Object == "admin":
            return True
        else:
            return False
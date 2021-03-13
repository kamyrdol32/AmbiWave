import re

Regex_Mail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(Type, Object):
    print(Type + " " + Object)
    if Type == "Mail":
        if re.search(Regex_Mail, Object) or Object == "admin":
            return True
        else:
            return False
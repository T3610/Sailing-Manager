from functools import wraps
from function import *
def pursuitOnly(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)
        mycursor.execute("SELECT raceType FROM racesconfig")
        data = mycursor.fetchone()
        if data[0] == "PURSUIT":
            return f(*args, **kwargs)
        else:
            return "This page is only used for pursuit races"
    return decorated_view

def handicapOnly(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)
        mycursor.execute("SELECT raceType FROM racesconfig")
        data = mycursor.fetchone()
        if data[0] == "HANDICAP":
            return f(*args, **kwargs)
        else:
            return "This page is only used for handicap races"
    return decorated_view
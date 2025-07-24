import mysql.connector 
from flask import g
import sqlite3

WORKBENCH_HOST =""
WORKBENCH_USERNAME = ""
WORKBENCH_PASS = ""

DB_LOCATION = ""

SQL_TYPE = ""

ISFLASK = ""




#DB NAME BLOCK
#when 
DB_NAME = ""

#holds name for SQL database
def get_DB_NAME(DataBase_Name):
    global DB_NAME
    DB_NAME = DataBase_Name

def USE_DB_NAME(DATA = DB_NAME):
    return DB_NAME
    





#DB LOCATION BLOCK:

def ADD_DB_LOCATION(location):
    global DB_LOCATION

    DB_LOCATION = location.upper()

#shows what orentation of db this is
def USE_DB_LOCATION(Location = DB_LOCATION):
    if Location.upper() == "LOCAL":
        return "LOCAL"
    elif Location == "WORKBENCH":
        return "WORKBENCH"
    else:
        raise ValueError(f"----ERROR---- The command: 'DB.BDLOCATION({Location})' cannot be intrepreted.\n current values are: 'LOCAL' or 'WOEKBENCH'")
    



#SQL TYPE BLOCK

def GET_SQL_TYPE(type):
    global SQL_TYPE

    SQL_TYPE = type


def USE_SQLTYPE(type = SQL_TYPE):
    if type.upper() == "SQLite":
        return "LITE"
    elif type.upper() == "SQL":
        return "SQL"
    else:
        raise ValueError(f"----ERROR----\nThe command: 'DB.ADD_SQLTYPE({type})' cannot be intrepreted.\n current values are: 'SQL' or 'SQLite'") 


#ISFLASK BLOCK

def ADD_ISFLASK(flask):
    global ISFLASK

    ISFLASK = flask

    
def USE_ISFLASK(Type = ISFLASK):
    if Type.upper() == "FLASK":
        return True
    elif Type.upper() == "OTHER":
        return False
    



#INITALIZATION BLOCK
    
#TIE THE FOLLOWIING TOW DEFS INTO LOCATION DEF -> CHECK IF POSSIBLE
# _LOCAL AND _WORKBENCH INITTALIZATION OF DB'S
#figureout a way to pass the get_DB_NAME as the DATABASE variable
#is equivelent to get_DB

def GET_WORKBENCH_INFO(HOST, USER_NAME, PASSWORD):
    global WORKBENCH_HOST
    global WORKBENCH_USERNAME
    global WORKBENCH_PASS

    WORKBENCH_HOST = HOST
    WORKBENCH_USERNAME = USER_NAME
    WORKBENCH_PASS = PASSWORD

def DB_INITALIZATION_LOCAL(DATABASE = DB_NAME):

    if DB_LOCATION != "LOCAL":
         raise ValueError(f"----ERROR----\nThe command: 'DB_INITALIZATION_WORKBENCH()' is not needed fot the data type of: {DB_LOCATION}")
    
    elif DB_LOCATION == "LOCAL" and ISFLASK == False:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        return conn, cursor
    
    elif DB_LOCATION == "LOCAL" and ISFLASK == True:
        if 'db' not in g:
            g.db = sqlite3.connect(DATABASE)
        db = g.db
        conn = g.db
        cursor = db.cursor()
        return conn, cursor
    else:
        raise ValueError(f"----ERROR----\nThe input in method:'DB_INITALIZATION_LOCAL({DATABASE})' is invalid\n check your values and please ensure that the 'ISFLASK()' method is filled out properly")

def DB_INITALIZATION_WORKBENCH():
    if DB_LOCATION == "LOCAL":
        raise ValueError(f"----ERROR----\nThe command: 'DB_INITALIZATION_WORKBENCH()' is not needed fot the data type of: {DB_LOCATION}")
    
    elif DB_LOCATION == "WORKBENCH" and ISFLASK == False:
        db = mysql.connector.connect(
            host = WORKBENCH_HOST,
            user = WORKBENCH_USERNAME,
            password = WORKBENCH_PASS,
            database = DB_NAME
        )
        cursor = db.cursor()
        return db, cursor

    elif DB_LOCATION == "WORKBENCH" and ISFLASK == True:
        if 'db' not in g:
            g.db = mysql.connector.connect(
                host = WORKBENCH_HOST,
                user = WORKBENCH_USERNAME,
                password = WORKBENCH_PASS,
                database = DB_NAME
            )
            db = g.db
            cursor = db.cursor()
        return g.db, cursor
    else:
        raise ValueError(f"----ERROR----\nThe input in method:'DB_INFO_WORKBENCH()' is invalid\n check your values within: 'GET_WORKBENCH_INFO'and please ensure that the 'ISFLASK()' method is filled out properly")

def close_connection(exception):
    db = g.pop('db', None)
    if db:
        db.close()
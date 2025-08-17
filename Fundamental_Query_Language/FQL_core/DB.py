import mysql.connector 
import sqlite3
#prevent crash form a NULL flask import
try:
    from flask import Flask, g
except ImportError:
    g= None
from pathlib import Path


WORKBENCH_HOST =""
WORKBENCH_USERNAME = ""
WORKBENCH_PASS = ""

DB_LOCATION = ""

SQL_TYPE = ""

ISFLASK = ""

PATH = ""

#gets path for SQLite functions (SQLITE ONLY)
def ADD_DB_PATH(pathUSE):
    global PATH
    PATH = pathUSE

def USE_DB_PATH():
    return USE_DB_PATH





#DB NAME BLOCK
#when 
DB_NAME = ""


def DEFAULT_TABLE(Table):
    return Table

#holds name for SQL database (SQL ONLY)
def get_DB_NAME(DataBase_Name):
    global DB_NAME
    DB_NAME = DataBase_Name

def USE_DB_NAME(DATA = DB_NAME):
    return DB_NAME
    


#DB LOCATION BLOCK:
#GET RID OF THIS FUNCTION, UNESSARCARY

def ADD_DB_LOCATION(location):
    global DB_LOCATION

    DB_LOCATION = location.upper()

#shows what orentation of db this is
#THINK ABOUT DELTEING THIS DUE TO SQL AND SQLite seperate
def USE_DB_LOCATION(Location = DB_LOCATION):
    if Location.upper() == "LOCAL":
        return "LOCAL"
    elif Location.upper() == "MYSQL":
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

#adds ISFLASK value to be implemented within the def's of WORKBENCH/LOCAL
def USE_ISFLASK(Type = ISFLASK):
    if Type.upper() == "FLASK":
        return True
    elif Type.upper() == "OTHER":
        return False
    



#INITALIZATION BLOCK
    
#TIE THE FOLLOWIING TOW DEFS INTO LOCATION DEF -> CHECK IF POSSIBLE
# _LOCAL AND _WORKBENCH INITTALIZATION OF DB'S
#is equivelent to get_DB

def GET_WORKBENCH_INFO(HOST, USER_NAME, PASSWORD):
    global WORKBENCH_HOST
    global WORKBENCH_USERNAME
    global WORKBENCH_PASS

    WORKBENCH_HOST = HOST
    WORKBENCH_USERNAME = USER_NAME
    WORKBENCH_PASS = PASSWORD

def lite_parent_confirm(path_):
    try:
        p = Path(path_)
    except:
        raise ValueError(f"----ERROR----\nThe PATH input of 'DB.ADD_DB_PATH()' is needed to initaliza a SQLite function")
    if p.parent and not p.parent.exists:
        p.parent.mkdir(parents=True, exist_ok=True)

def db_initalization_helper():
    lite_parent_confirm(PATH)
    conn = sqlite3.connect(PATH)
    
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")   # better concurrency
    conn.execute("PRAGMA synchronous = NORMAL;")

    return conn



#add SQL compatability to local initalization
def DB_INITALIZATION_LOCAL(DATABASE = DB_NAME):

    if DB_LOCATION != "LOCAL":
        raise ValueError(
            "----ERROR----\n"
            "'DB_INITIALIZATION_LOCAL()' is only for DB_LOCATION='LOCAL' "
            f"(current: {DB_LOCATION})"
        )
    if USE_SQLTYPE != "LITE":
        raise ValueError(
            "----ERROR----\n"
            "DB_INITIALIZATION_LOCAL requires SQLite (USE_SQLTYPE='LITE'), "
            f"got: {USE_SQLTYPE}"
        )

    # Non-Flask path
    if not ISFLASK:
        conn = db_initalization_helper(DATABASE)
        return conn, conn.cursor()

    # Flask path (one connection per request)
    if ISFLASK:
        if g is None:
            raise RuntimeError(
                "ISFLASK=True but Flask isn't available. Install Flask or set ISFLASK=False."
            )
        if 'db' not in g:
            g.db = db_initalization_helper(DATABASE)
        conn = g.db
        return conn, conn.cursor()




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
        if g == None:
            raise RuntimeError(f"----ERROR----\nThe import of: 'from flask import g' was not found.\nMake sure pip is insatlled on your device and run the command of: 'pip install flask' ")
        if 'db' not in g:
            g.db = mysql.connector.connect(
                host = WORKBENCH_HOST,
                user = WORKBENCH_USERNAME,
                password = WORKBENCH_PASS,
                database = DB_NAME
            )
            cursor = g.db.cursor()
        return g.db, cursor
    else:
        raise ValueError(f"----ERROR----\nThe input in method:'DB_INFO_WORKBENCH()' is invalid\n check your values within: 'GET_WORKBENCH_INFO'and please ensure that the 'ISFLASK()' method is filled out properly")

def close_connection(exception):
    db = g.pop('db', None)
    if db:
        db.close()
import mysql.connector 
from flask import g
import sqlite3

WORKBENCH_HOST =""
WORKBENCH_USERNAME = ""
WORKBENCH_PASS = ""

#holds name for SQL database
def get_DB_NAME(DataBase_Name):
    return DataBase_Name   


#shows what orentation of db this is
def DB_LOCATION(Location):
    if Location.upper() == "LOCAL":
        return "LOCAL"
    elif Location.uppper == "WORKBENCH":
        return "WORKBENCH"
    else:
        raise ValueError(f"----ERROR---- The command: 'DB.BDLOCATION({Location})' cannot be intrepreted.\n current values are: 'LOCAL' or 'WOEKBENCH'")
    

#weather the user is using an SQL or SQLite application, to be used in hardcode
def SQL_TYPE(Type):
    if Type.upper() == "SQLite":
        return"LITE"
    elif Type.upper() == "SQL":
        return "SQL"
    else:
        raise ValueError(f"----ERROR----\n THE VALUE OF 'DB.SQL_TYPE({type})' CANNOT BE IDENTIFYED\n MUST BE OF VALUE 'SQL'  OR 'SQLite'")
    
def ISFLASK(Type):
    if Type.upper() == "FLASK":
        return True
    elif Type.upper() == "OTHER":
        return False
    
    
#TIE THE FOLLOWIING TOW DEFS INTO LOCATION DEF -> CHECK IF POSSIBLE
# _LOCAL AND _WORKBENCH INITTALIZATION OF DB'S
#figureout a way to pass the get_DB_NAME as the DATABASE variable
#is equivelent to get_DB

def GET_WORKBENCH_INFO(HOST, USER_NAME, PASSWORD):
    WORKBENCH_HOST = HOST
    WORKBENCH_USERNAME = USER_NAME
    WORKBENCH_PASS = PASSWORD

def DB_INITALIZATION_LOCAL(DATABASE = get_DB_NAME):

    if DB_LOCATION != "LOCAL":
         raise ValueError(f"----ERROR----\nThe command: 'DB_INITALIZATION_WORKBENCH()' is not needed fot the data type of: {DB_LOCATION}")
    
    elif DB_LOCATION == "LOCAL" and ISFLASK == False:
        conn = sqlite3.connect(DATABASE)
        return conn.cursor()
    
    elif DB_LOCATION == "LOCAL" and ISFLASK == True:
        if 'db' not in g:
            g.db = sqlite3.connect(DATABASE)
        db = g.db
        return db.cursor()
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
            database = get_DB_NAME
        )
        cursor = db.cursor()

    elif DB_LOCATION == "WORKBENCH" and ISFLASK == True:
        if 'db' not in g:
            g.db = mysql.connector.connect(
                host = WORKBENCH_HOST,
                user = WORKBENCH_USERNAME,
                password = WORKBENCH_PASS,
                database = get_DB_NAME
            )
        return g.db
    else:
        raise ValueError(f"----ERROR----\nThe input in method:'DB_INFO_WORKBENCH()' is invalid\n check your values within: 'GET_WORKBENCH_INFO'and please ensure that the 'ISFLASK()' method is filled out properly")

def close_connection(exception):
    db = g.pop('db', None)
    if db:
        db.close()
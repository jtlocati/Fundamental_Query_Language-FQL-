import mysql.connector 
from flask import g
import sqlite3

#holds name for SQL database
def DB_NAME(DataBase_Name):
    return DataBase_Name    
    
    
#shows what orentation of db this is
def DB_LOCATION(Location):
    if Location.upper == "LOCAL":
        return "LOCAL"
    elif Location.uppper == "WORKBENCH":
        return "WORKBENCH"
    elif(Location.upper == "FLASK"):
        return "FLASK"
    else:
        return ValueError(f"----ERROR---- The command: 'DB.BDLOCATION({Location})' cannot be intrepreted.\n current values are: 'LOCAL' or 'WOEKBENCH'")
    

#weather the user is using an SQL or SQLite application
def SQL_TYPE(Type):
    if Type.upper == "SQLite":
        return"lite"
    elif Type.upper == "SQL":

        return ValueError(f"----ERROR----\n THE VALUE OF 'DB.SQL_TYPE({type})' CANNOT BE IDENTIFYED\n MUST BE OF VALUE 'SQL'  OR 'SQLite'")
    
    
#TIE THE FOLLOWIING TOW DEFS INTO LOCATION DEF -> CHECK IF POSSIBLE
# _LOCAL AND _WORKBENCH INITTALIZATION OF DB'S
def DB_INITALIZATION_LOCAL(DATA_BASE):
    if DB_LOCATION != "LOCAL":
        return ValueError(f"----ERROR----\nThe command: 'DB_INITALIZATION_WORKBENCH()' is not needed fot the data type of: {DB_LOCATION}")
    
    else:
        conn = sqlite3.connect(DATA_BASE)
    

def DB_INFO_WORKBENCH(HOST, USER_NAME, PASSWORD):
    if DB_LOCATION == "LOCAL":
        return ValueError(f"----ERROR----\nThe command: 'DB_INITALIZATION_WORKBENCH()' is not needed fot the data type of: {DB_LOCATION}")
    
    elif DB_LOCATION == "WORKBENCH":
        db = mysql.connector.connect(
            host = HOST,
            user = USER_NAME,
            password = PASSWORD,
            database = DB_NAME
        )
        cursor = db.cursor()

    elif DB_LOCATION == "FLASK":
        if 'db' not in g:
            g.db = mysql.connector.connect(
                host = HOST,
                user = USER_NAME,
                password = PASSWORD,
                database = DB_NAME
            )
        return g.db

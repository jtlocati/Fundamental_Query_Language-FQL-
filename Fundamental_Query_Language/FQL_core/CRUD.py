import DB
import sqlite3
import mysql.connector
from flask import g

"--------------The Command of 'CRUD' Is invalad and must be followed with a CRUD command--------------"

if DB.DB_LOCATION == "LOCAL":
    db = DB.DB_INITALIZATION_LOCAL
else:
    db = DB.DB_INITALIZATION_WORKBENCH

cursor = db.cursor()

def INSERT_INTO(table, cols, values):
    if len(cols) != len(values):
        raise ValueError(f"----ERROR----\nThe values of {cols} and {values} must be equal")
    #holds values for %s / ?
    pers = []
    for _ in range(len(values)):
        if DB.SQL_TYPE == "SQL":
            Placeholders = ", ".join(["%s"] *  len(values))
        elif DB.SQL_TYPE == "LITE":
            Placeholders = ", ".join(["?"] *  len(values))
        else:
            raise ValueError(f"----ERROR----\nthe statment of 'INSERT_INTO({table}, {cols}, {values}) is not in correct format\n check values again and rerun")
        
    col_str = ", ".join(cols)
    query = (f"INSERT INTO {table} ({col_str}) values ({Placeholders})")
    cursor.execute(query, values)
    if DB.DB_LOCATION == "LOCAL":
        db.commit()
    else:
        db.commit()




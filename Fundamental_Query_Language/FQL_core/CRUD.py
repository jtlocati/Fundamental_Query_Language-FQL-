import DB
import sqlite3
import mysql.connector
from flask import g

"--------------The Command of 'CRUD' Is invalad and must be followed with a CRUD command--------------"


#INITALIZATION of both cursor and db.(condition) varibles
if DB.USE_DB_LOCATION() == "LOCAL":
    conn, cursor = DB.DB_INITALIZATION_LOCAL()
    cursor = conn.cursor()
else:
    db, cursor = DB.DB_INITALIZATION_WORKBENCH()


def INSERT_INTO(table, cols, values):
    if len(cols) != len(values):
        raise ValueError(f"----ERROR----\nThe values of {cols} and {values} must be equal")
    #holds values for %s / ?
    pers = []
    for _ in range(len(values)):
        if DB.ADD_SQLTYPE() == "SQL":
            Placeholders = ", ".join(["%s"] *  len(values))
        elif DB.ADD_SQLTYPE() == "LITE":
            Placeholders = ", ".join(["?"] *  len(values))
        else:
            raise ValueError(f"----ERROR----\nthe statment of 'INSERT_INTO({table}, {cols}, {values}) is not in correct format\n check values again and rerun")
        
    col_str = ", ".join(cols)
    query = (f"INSERT INTO {table} ({col_str}) values ({Placeholders})")
    cursor.execute(query, values)
    if DB.USE_DB_LOCATION() == "LOCAL":
        conn.commit()
        conn.close()
    else:
        db.commit()
        db.close()




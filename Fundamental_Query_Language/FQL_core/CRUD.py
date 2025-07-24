import DB
import sqlite3
import mysql.connector
from flask import g

"--------------The Command of 'CRUD' Is invalad and must be followed with a CRUD command--------------"
#raise ValueError(f"----ERROR----\nThe input of 'CRUD.INSERT_INTO({table}, {cols}, {values})' is not valid\nThe number of values within the col value and 'value' value are not equivelent, pelase check values and try again.")

#INITALIZATION of both cursor and db.(condition) varibles
if DB.USE_DB_LOCATION() == "LOCAL":
    conn, cursor = DB.DB_INITALIZATION_LOCAL()
    cursor = conn.cursor()
else:
    db, cursor = DB.DB_INITALIZATION_WORKBENCH()


def INSERT_INTO(table, cols, values):
    placeholders = ""
    multipule = False
    placee = ""

    for row in values:
        length = len(row)
        if length != len(cols):
            break
        else:
            multipule = True

    #Finds the 
    if DB.USE_SQLTYPE() == "LITE":
        placee = "?"
    
    else:
        placee = "%s"
    
    if multipule == True:
        placeholders = ", ".join(["(" + ", ".join([placee] * len(values[0])) + ")"] * len(values))

    else:
        placeholders = "("
        for _ in values:
            placeholders += (f"{placee},")
        placeholders = placeholders[:-1]
        placeholders += ")"

    query = (f"INSERT INTO {table} ({cols}) VALUES {placeholders}")
    flat_Values = [val for row in values for val in row]
    if flat_Values == 1:
        flat_Values += ","

    cursor.execute(query, flat_Values)

    if DB.USE_DB_LOCATION == "LOCAL":
        conn.commit()
        conn.close()
    else:
        db.commit()
        db.close()


def SELECT_FROM(table, cols, specifications, LIMIT):
    #cols and specification must be string, and seperated via ','
    if cols == "*" or cols.upper() == "ALL":
        cols = "*"
    else:
        cols = cols.lower()
    
    if len(LIMIT) <= 0:
        LIMIT = 500


    query =(f"SELECT {cols} FROM {table} WHERE {specifications} LIMIT {LIMIT}")

    cursor.execute(query)
    result = cursor.fetchall()

    if DB.USE_DB_LOCATION() == "LOCAL":
        #commit is only used when making changes to a table
        conn.close()
    else:
        db.close()

    return result



def SELECT_SORTED(table, cols, Group, WHERE, LIMIT):
    if cols == "*" or cols.upper() == "ALL":
        cols = "*"
    else:
        cols = cols.lower()

    if len(LIMIT) <= 0:
        LIMIT = 500
    
    #make sure that the WHERE cluase is dynamic
    query = (f"SELECT {cols} FROM {table} WHERE {WHERE} GROUP BY {Group}")

    cursor.execute(query)
    result = cursor.fetchall()

    if DB.USE_DB_LOCATION == "LOCAL":
        conn.close()
    else:
        db.close()
    return result



def SELECT_SORTED_ADVANCED(Table, cols, new_col, new_col_specifications, Group, specifications, LIMIT):
    if cols == "*" or cols.upper() == "ALL":
        cols = "*"
    else:
        cols = cols.lower()

    if len(LIMIT) == 0:
        LIMIT = 500
    
    new_col = new_col.lower()
    Group = Group.lower()

    query = (f"SELECT {cols}, {new_col_specifications} AS {new_col} FROM {Table} GROUP BY {Group} HAVING {specifications} LIMIT {LIMIT}")

    cursor.execute(query)
    result = cursor.fetchall()

    if DB.USE_DB_LOCATION == "LOCAL":
        conn.close()
    else:
        db.close()
    
    return result
 
    
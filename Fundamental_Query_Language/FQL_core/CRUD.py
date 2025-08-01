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

#.DELETE BLOCK

def ROW_DELETE(Table, Specification):

    if len(Specification) >= 0:
        raise ValueError (f"----ERROR----\n The method of 'ROW_DELETE({Table}, {Specification})' is not valid\n3rd 'Specification' value must be filled out")
    
    query = (f"DELETE FROM {Table} WHERE {Specification}")

    cursor.execute(query)

    if DB.USE_DB_LOCATION == "LOCAL":
        conn.commit()
        conn.close()
    else:
        db.commit()
        db.close()


def RETURN_DELETED(Table, col, condition):
    query = (f"SELECT * FROM {Table} WHERE {condition}")
    cursor.execute(query)
    ret = cursor.fetchall()

    query_two = (f"DELETE FROM {Table} WHERE {condition}")
    cursor.execute(query_two)

    if DB.USE_DB_LOCATION() == "LOCAL":
        conn.commit()
        conn.close()
    else:
        db.commit()
        db.close()

    return ret


def CLEAR_TABLE(Table):
    query = (f"DELETE FROM {Table}")
    cursor.execute(query)

    if DB.USE_DB_LOCATION() == "LOCAL":
        conn.commit()
        conn.close()
    else:
        db.commit()
        db.close()


#GPT walthrough needed, CONTINUE AT LATER TIME 
def JOIN_DELETE(Primary, Target_tables, join_on, Clause):

    query = ""
    joiner = ""

    if DB.USE_SQLTYPE() == "LITE" and (Target_tables > 2 or join_on > 2):
        raise ValueError(f"----ERROR----\nThe function of 'CRUD.JOIN_DELETE({Primary}, {Target_tables}, {join_on})' cannot be satisfied\nSQLite cannot handle the joining of more than 2 tables")
    elif len(Target_tables) != len(join_on):
        raise ValueError(f"----ERROR----\nThe ststment: 'CRUD.JOIN_DELETE({Primary}, {Target_tables}, {join_on})")

    if len(Target_tables) == 2:
        """query = (f"SELECT {Target_tables[0]} FROM {Target_tables[0]} JOIN {Target_tables[1]} ON {Target_tables[0]}.{join_on[0]} = {Target_tables[1]}.{join_on[1]} WHERE {Clause}")"""
        #make dynamic for multipule tables
    else:
        for i in range(len(Target_tables)):
            joiner += (f"JOIN {Target_tables[i]} ON {Target_tables[i]}.{join_on[i]}")


    

    return "filler"

def DELETE_COL(Table, cols_to_drop):
    DCols = ""
    RCols = ""

    #query = (f"ALTER TABLE {Table}\nDROP COLUMN {col}")
    #cursor.execute(query)

    if DB.USE_SQLTYPE() == "SQL":
        for value in cols_to_drop:
            DCols += (F"DROP COLUMN {value},")
        DCols = DCols[:-1]
        query = (f"ALTER TABLE {Table} ")
        query += DCols

    else:
        #returns col info
        cursor.execute(f"PRAGMA table_info({Table})")
        table_info = cursor.fetchall()

        #FIND WAYS TO ELEIMINATE THIS SECTION
        print("[DEBUG] Table Info:", table_info)
        print("[DEBUG] First Row Type:", type(table_info[0]) if table_info else "Empty")
        exit()

        for col in table_info:
            col_name = col[1]
            col_type = col[2]
            if col_name not in cols_to_drop:
                RCols += col_name
        RCols = RCols.rstrip(", ")
    

    if DB.USE_DB_LOCATION() == "LOCAL":
        conn.commit()
        conn.close()
    else:
        db.commit()
        db.close()


def LIMIT_DELETE(Table, Order, Limit):
    return "filler"

def DELETE_IN(Table, col, condition):
    return "filler"

def MULTI_DELETE(Table, col, values):
    return "filler"


    
 
    
import DB
import sqlite3

"--------------The Command of 'CRUD' Is invalad and must be followed with a CRUD command--------------"
SQL_Version = DB.SQL_TYPE

def INSERT(Table, columns, values):
    if Table == None:
        Table = DB.DEFAULT_DB
    PER_S = 0
    col_Str = ",".join(columns)

    placeholders = ", ".join(["%s"] * len(values))

    query = f"INSERT INTO {Table} ({col_Str}) VALUES ({placeholders})"

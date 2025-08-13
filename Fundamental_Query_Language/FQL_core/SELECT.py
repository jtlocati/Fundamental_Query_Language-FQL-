import DB

if DB.USE_DB_LOCATION() == "LOCAL":
    conn, cursor = DB.DB_INITALIZATION_LOCAL()
else:
    db, cursor = DB.DB_INITALIZATION_WORKBENCH()


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
import DB
if DB.USE_DB_LOCATION() == "LOCAL":
    conn, cursor = DB.DB_INITALIZATION_LOCAL()
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
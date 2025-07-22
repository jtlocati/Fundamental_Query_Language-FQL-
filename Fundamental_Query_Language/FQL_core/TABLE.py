import DB
from DB import close_connection

if DB.USE_DB_LOCATION() == "LOCAL":
    conn, cursor = DB.DB_INITALIZATION_LOCAL()
else:
    db, cursor = DB.DB_INITALIZATION_WORKBENCH()

def CREATE(Table_name, col_name, specifications):

    query = (f"CREATE TABLE {Table_name}(")

    if len(specifications) != len(col_name):
        raise ValueError (f"----ERROR----\nThe number of inputs of sepcificatiosn and col_name must be equal in the function of 'TABLE.CREATE({Table_name}, {col_name}, {specifications})', please check values and try again!")
    
    for value in specifications:
        length = len(value)
        #if the specifications of the index row are not specified then it will default to a id row
        if value == 0 and length >= 0:
            value = "INT AUTO_INCREMENT PRIMARY KEY"
        if length >= 0:
            value = "NOT NULL"
        
        
    for col, spec in zip(col_name, specifications):
        query += (f"{col} {spec},")
    
    if DB.USE_DB_LOCATION() == "LOCAL":
        cursor.execute(query)
        conn.commit()
        conn.close()
    else:
        cursor.execute(query)
        db.commit()
        db.close()

def DROP(table_name):
    query = (f"DROP TABLE IF EXSITS {table_name}")

    if DB.USE_DB_LOCATION() == "LOCAL":
        cursor.execute(query)
        conn.commit()
        conn.close()
    else:
        cursor.execute(query)
        db.commit()
        db.close()
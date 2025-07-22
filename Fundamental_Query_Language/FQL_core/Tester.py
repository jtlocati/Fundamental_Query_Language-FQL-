import DB
import CRUD
from DB import close_connection

DB.get_DB_NAME("parks_and_rec.db")
DB.GET_WORKBENCH_INFO("jetlocati.com", "jet_locati", "Ours4922")
DB.ADD_ISFLASK("OTHER")

condition = 0
data = 400

if data != 400:
    print("somthing is wrong")
else:
    CRUD.INSERT_INTO("employee_data", ["employeename", "emplyee_job"], [condition, "name"])
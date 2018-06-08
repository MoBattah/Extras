import sys
import pyodbc
from flask import Flask, request, abort
import datetime

app = Flask(__name__)

global pingdomlogfile
pingdomlogfile = "E:\\Web\\PingdomWebHook\\PingdomWebHookLog.log"
@app.route('/', methods=['POST'])
def main():
    sys.stdout = open(pingdomlogfile, 'a')  ###LOGGING
    print("Start: ", str(datetime.datetime.now()).split('.')[0])
    print("Webhook started");
    if request.method == 'POST':
        print("Recieved POST")
        print(request.json)
        gatherParameters()
        return '', 200
    else:
        print("Recieved something other than POST.")
        abort(400)
    sys.stdout.close()  ###LOGGING
    main()

def gatherParameters():
    print("GatherParameters")
    check_id = fetchParameter("check_id")
    print("Fetch check_id")
    check_type = fetchParameter("check_type")
    print("Fetch check_type")
    hostname = request.json["check_params"]["hostname"]
    print("Fetch hostname")
    try: full_url = request.json["check_params"]["full_url"]
    except KeyError:
        full_url = hostname
    print("Fetch url")
    previous_state = fetchParameter("previous_state")
    print("Fetch prev state")
    current_state = fetchParameter("current_state")
    print("Fetch current state")
    importance_level = fetchParameter("importance_level")
    state_changed_timestamp = fetchParameter("state_changed_timestamp")
    state_changed_utc_time = fetchParameter("state_changed_utc_time")
    check_name = fetchParameter("check_name")
    long_description = fetchParameter("long_description")
    description = fetchParameter("description")
    sqlStatement = "INSERT INTO WebHookTestTable (check_id, check_name, check_type, full_url, hostname, previous_state, current_state, importance_level, state_changed_timestamp, state_changed_utc_time, long_description, description) " \
                   "VALUES(\'"+check_id+"\',\'"+check_name+"\',\'"+check_type+"\',\'"+full_url+"\',\'"+hostname+"\',\'"+previous_state+"\',\'"+current_state+"\',\'"+importance_level+"\',\'"+state_changed_timestamp+"\',\'"+state_changed_utc_time+"\',\'"+long_description+"\',\'"+description+"\')"
    SQLExecute(sqlStatement)
    print("Executed "+sqlStatement)


def fetchParameter(columnname):
    print("fetchParameter")
    param = request.json[str(columnname)]
    param = str(param)
    return param


def SQLExecute(executestring):
    print("SQLExecute")
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=devops01test.database.windows.net;'
        r'DATABASE=TestWebHookDB;'
        r'UID=user;'
        r'PWD=pass'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print(executestring)
    cursor.execute("" + executestring + "")
    print("SQL executed")


if __name__ == '__main__':
    app.run('0.0.0.0',8083)

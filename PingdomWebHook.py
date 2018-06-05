import sys
import pyodbc
from flask import Flask, request, abort
import logging

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    logging.basicConfig(filename='C:\\Users\\mo.battah\\Documents\\PingdomAPI.log', level=logging.DEBUG)
    print("Webhook started");
    #logging.debug(sys.stdout.flush())
    logging.debug("Webhook started")
    if request.method == 'POST':
        logging.debug("Recieved POST")
        logging.debug(request.json)
        gatherParameters()
        return '', 200
    else:
        logging.debug("Recieved something other than POST")
        abort(400)
    main()

def gatherParameters():
    logging.debug("gatherParameters")
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
    sqlStatement = "INSERT INTO WebHookTestTable (check_id, check_name, check_type, full_url, hostname, previous_state, current_state, importance_level, state_changed_timpstamp, state_changed_utc_time, long_description, description) " \
                   "VALUES(\'"+check_id+"\',\'"+check_name+"\',\'"+check_type+"\',\'"+full_url+"\',\'"+hostname+"\',\'"+previous_state+"\',\'"+current_state+"\',\'"+importance_level+"\',\'"+state_changed_timestamp+"\',\'"+state_changed_utc_time+"\',\'"+long_description+"\',\'"+description+"\')"
    SQLExecute(sqlStatement)
    logging.debug("Executed "+sqlStatement)


def fetchParameter(columnname):
    logging.debug("fetchParameter")
    param = request.json[str(columnname)]
    param = str(param)
    return param


def SQLExecute(executestring):
    logging.debug("SQLExecute")
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=devops01test.database.windows.net;'
        r'DATABASE=TestWebHookDB;'
        r'UID=user;'
        r'PWD=pass'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    logging.debug(executestring)
    print(executestring)
    cursor.execute("" + executestring + "")
    logging.debug("SQL executed")


if __name__ == '__main__':
    app.run('0.0.0.0',8083)
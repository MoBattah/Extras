import sys
import pyodbc
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    print("Webhook started"); sys.stdout.flush()
    if request.method == 'POST':
        gatherParameters()
        return '', 200
    else:
        abort(400)

def gatherParameters():
    check_id = fetchParameter("check_id")
    check_type = fetchParameter("check_type")
    hostname = request.json["check_params"]["hostname"]
    full_url = request.json["check_params"]["full_url"]
    previous_state = fetchParameter("previous_state")
    current_state = fetchParameter("current_state")
    importance_level = fetchParameter("importance_level")
    state_changed_timestamp = fetchParameter("state_changed_timestamp")
    state_changed_utc_time = fetchParameter("state_changed_utc_time")
    check_name = fetchParameter("check_name")
    long_description = fetchParameter("long_description")
    description = fetchParameter("description")
    sqlStatement = "INSERT INTO WebHookTestTable (check_id, check_name, check_type, full_url, hostname, previous_state, current_state, importance_level, state_changed_timpstamp, state_changed_utc_time, long_description, description) " \
                   "VALUES(\'"+check_id+"\',\'"+check_name+"\',\'"+check_type+"\',\'"+previous_state+"\',\'"+current_state+"\',\'"+full_url+"\',\'"+hostname+"\',\'"+importance_level+"\',\'"+state_changed_timestamp+"\',\'"+state_changed_utc_time+"\',\'"+long_description+"\',\'"+description+"\')"
    SQLExecute(sqlStatement)


def fetchParameter(columnname):
    param = request.json[str(columnname)]
    param = str(param)
    return param


def SQLExecute(executestring):
    conn = pyodbc.connect(r'DSN=TestWebHookDB;UID=mo.battah;PWD=pass')
    conn.autocommit = True
    cursor = conn.cursor()
    print(executestring)
    cursor.execute("" + executestring + "")


if __name__ == '__main__':
    app.run()

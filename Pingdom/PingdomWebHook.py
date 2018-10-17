import sys
import pyodbc
from flask import Flask, request, abort
import datetime
import config

app = Flask(__name__)

global pingdomlogfile
pingdomlogfile = config.CONFIG['LogFileLocation']



@app.route('/', methods=['POST'])
def main():
    if request.method == 'POST':
        sys.stdout = open(pingdomlogfile, 'a+')  #LOGGING
        print("POST: ", str(datetime.datetime.now()).split('.')[0])
        print(request.json)
        gatherParameters()
        return '', 200
    else:
        print("Recieved something other than POST.")
        abort(400)
    sys.stdout.close()  ###LOGGING


def gatherParameters():
    print("GatherParameters")
    check_id = fetchParameter("check_id")
    print("Fetch check_id")
    check_type = fetchParameter("check_type")
    print("Fetch check_type")
    hostname = request.json["check_params"]["hostname"]
    print("Fetch hostname")
    try:
        full_url = request.json["check_params"]["full_url"]
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
    sqlStatement = "INSERT INTO WebHookPingdomTemp (check_id, check_name, check_type, full_url, hostname, previous_state, current_state, importance_level, state_changed_timestamp, state_changed_utc_time, long_description, description) " \
                   "VALUES(\'" + check_id + "\',\'" + check_name + "\',\'" + check_type + "\',\'" + full_url + "\',\'" + hostname + "\',\'" + previous_state + "\',\'" + current_state + "\',\'" + importance_level + "\',\'" + state_changed_timestamp + "\',\'" + state_changed_utc_time + "\',\'" + long_description + "\',\'" + description + "\')"
    SQLExecute(sqlStatement)
    print("Sent to be executed: " + sqlStatement)


def fetchParameter(columnname):
    param = request.json[str(columnname)]
    param = str(param)
    return param


def SQLExecute(executestring):
    connection_string = "DRIVER={ODBC Driver 17 for SQL Server}; " + "SERVER=" + config.CONFIG['Server'] + ";DATABASE=" + config.CONFIG['Database'] + ";UID=" + config.CONFIG['UID'] + ";PWD=" + config.CONFIG['PWD']
    conn = pyodbc.connect(connection_string)
    conn.autocommit = True
    cursor = conn.cursor()
    print(executestring)
    cursor.execute("" + executestring + "")
    print("SQL executed")


@app.route('/internalcheck.html')
def internalcheck():
    sys.stdout = open(pingdomlogfile, 'a+')  ###LOGGING
    print("Start: ", str(datetime.datetime.now()).split('.')[0])
    print("Internal check page triggered")
    sys.stdout.close()  ###LOGGING
    return 'Site is up'

if __name__ == '__main__':
    app.run('0.0.0.0', 8088)

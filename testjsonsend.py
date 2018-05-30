import sys
import pyodbc
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    print("webhook"); sys.stdout.flush()
    if request.method == 'POST':
        gatherParameters()
        return '', 200
    else:
        abort(400)

def gatherParameters():
    check_id = createStatement("check_id")
    check_type = createStatement("check_type")
    previous_state = createStatement("previous_state")
    sqlStatement = "INSERT INTO WebHookTestTable (check_id, check_type, previous_state) VALUES(\'"+check_id+"\',\'"+check_type+"\',\'"+previous_state+"\') "
    SQLExecute(sqlStatement)


def createStatement(columnname):
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

import sys
import pyodbc
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    print("webhook"); sys.stdout.flush()
    if request.method == 'POST':
        stdstatement("check_id")
        stdstatement("check_type")
        stdstatement("previous_state")
        return '', 200
    else:
        abort(400)


def stdstatement(columnname):
    param = request.json[str(columnname)]
    param = str(param)
    stdstatement1 = "INSERT INTO WebHookTestTable ("+columnname+") VALUES(\'"+param+"\')"
    stdstatement1 = str(stdstatement1)
    print(stdstatement1)
    SQLExecute(stdstatement1)

def SQLExecute(executestring):
    conn = pyodbc.connect(r'DSN=TestWebHookDB;UID=mo.battah;PWD=pass')
    conn.autocommit = True
    cursor = conn.cursor()
    print(executestring)
    cursor.execute("" + executestring + "")


if __name__ == '__main__':
    app.run()

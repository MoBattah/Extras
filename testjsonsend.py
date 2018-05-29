
import sys
import json
import pyodbc
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    print("webhook"); sys.stdout.flush()
    conn = pyodbc.connect(r'DSN=TestWebHookDB;UID=mo.battah;PWD=password')
    conn.autocommit = True
    if request.method == 'POST':
        sqlstatement = stdstatement("check_id")
        cursor = conn.cursor()
        cursor.execute(""+sqlstatement+"")
        return '', 200
    else:
        abort(400)


def stdstatement (columnname):
    param = request.json[str(columnname)]
    param = str(param)
    stdstatement1 = "INSERT INTO WebHookTestTable ("+columnname+") VALUES("+param+")"
    stdstatement1 = str(stdstatement1)
    return stdstatement1

if __name__ == '__main__':
    app.run()

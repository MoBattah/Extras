
import sys
import json
import pyodbc
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    print("webhook"); sys.stdout.flush()
    conn = pyodbc.connect(r'DSN=TestWebHookDB;UID=user;PWD=password')
    conn.autocommit = True
    if request.method == 'POST':
        check_id = request.json['check_id'] #get the value
        #check_id = str(check_id) #sql column is nvarcharmax wont take integers
        sqlstatement = stdstatement("check_id", check_id)
        cursor = conn.cursor()
        # sqlstatement = "INSERT INTO WebHookTestTable (check_id) VALUES ("+check_id+")"
        # sqlstatement = str(sqlstatement)
        cursor.execute(""+sqlstatement+"")
        # check_type = request.json['check_type']
        #


        return '', 200
    else:
        abort(400)

def stdstatement (columnname, param):
    param = str(param)
    stdstatement1 = "INSERT INTO WebHookTestTable ("+columnname+") VALUES("+param+")"
    stdstatement1 = str(stdstatement1)
    return stdstatement1

if __name__ == '__main__':
    app.run()

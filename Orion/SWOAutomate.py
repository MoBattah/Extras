import textwrap
import pyodbc
import sys
import datetime

global logfile
logfile = "C:\\Users\\mo.battah\\orionlogfile"

def main():

    sys.stdout = open(logfile, 'w+')
    print("Start: ", str(datetime.datetime.now()).split('.')[0])
    cursor = SQLExecute("SELECT [VolumeType], [FullName],[VolumePercentUsed] FROM [SW_ORION_PROD].[dbo].[Volumes] WHERE VolumePercentUsed >= '90'")
    getavg(cursor)
    cursor = SQLExecute("SELECT [VolumeType], [FullName],[VolumePercentUsed] FROM [SW_ORION_PROD].[dbo].[Volumes] WHERE VolumePercentUsed >= '90'")
    shrinkSQLlogs(cursor)
    sys.stdout.close()


def SQLExecute(executestring):
    print("SQLExecute")
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'DSN=USEGSQLWP001;'
        r'SERVER=USEGSQLWP001.vistex.local;'
        r'Trusted_Connection=yes;')
    #conn.autocommit = True
    cursor = conn.cursor()
    print(executestring)
    cursor.execute("" + executestring + "")
    print("SQL Executed")
    return(cursor)


def shrinkSQLlogs(cursor):
    sqlboxes = []
    for row in cursor: #print rows greater than a threshold if you'd like by limiting row[2]
        astring = row[1].split('-')[0]#geting only the hostname
        if 'SQL' in astring:
            sqlboxes.append(astring) #getting list of only SQL boxes
    print(sqlboxes, len(sqlboxes))#for logging
    sqlboxes = set(sqlboxes)
    print(sqlboxes, len(sqlboxes))

    for row in sqlboxes:
        print("Going to this server:", row)
        try: connecttoremote(row)
        except pyodbc.OperationalError as e:
            print("Some operational error occurred here, probably did not connect. ")
            print(e)





def create_query_string(sql_full_path, cursor):
    with open(sql_full_path, 'r') as f_in:
        lines = f_in.read()

        query_string = textwrap.dedent("""{}""".format(lines))
        cursor.execute(query_string)
        try:
            for row in cursor:
                print(row)
        except pyodbc.ProgrammingError as e:
            print(e)


def connecttoremote(hostname):
    cnxn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'DSN=USEGSQLWP001;'
        r'SERVER='+hostname+'.vistex.local;'
        r'Trusted_Connection=yes;')
    print("Connection information")
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM sys.databases")
    for row in cursor:
        print(row)
    create_query_string(r"C:\Users\mo.battah\Desktop\Reporting_DatabaseFileSize.sql", cursor)
    create_query_string(r"C:\Users\mo.battah\Desktop\Maintenance_ShrinkAllLogFiles.sql", cursor)
    create_query_string(r"C:\Users\mo.battah\Desktop\Maintenance_ShrinkAllDataFiles.sql", cursor)
    create_query_string(r"C:\Users\mo.battah\Desktop\Reporting_DatabaseFileSize.sql", cursor)

def getavg(cursor):
    count = 0
    total = 0
    for row in cursor:
        total = row[2] + total
        count = count + 1
    avg = total / count
    print("The average disk load: ", avg, "%")
main()

import textwrap
import pyodbc

def main():

    cursor = SQLExecute("SELECT [VolumeType], [FullName],[VolumePercentUsed] FROM [SW_ORION_PROD].[dbo].[Volumes] WHERE VolumePercentUsed >= '90'")
    shrinkSQLlogs(cursor)
    #query_string = create_query_string(r"C:\Users\mo.battah\Desktop\Maintenance_ShrinkAllLogFiles.sql")


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
        print("Going to this row:", row)
        connecttoremote(row)





def create_query_string(sql_full_path):
    with open(sql_full_path, 'r') as f_in:
        lines = f_in.read()

        query_string = textwrap.dedent("""{}""".format(lines))
        return query_string


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
    query_string = create_query_string(r"C:\Users\mo.battah\Desktop\Maintenance_ShrinkAllLogFiles.sql")
    cursor.execute(query_string)

main()

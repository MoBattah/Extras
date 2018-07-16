# #SQL_Query = "SELECT Type,FullName,VolumePercentUsed FROM Orion.Volumes WHERE VolumePercentUsed >= '90'"
#
# from sqlalchemy import create_engine
#


import pyodbc

def main():

    SQLExecute("SELECT [VolumeType], [FullName],[VolumePercentUsed] FROM [SW_ORION_PROD].[dbo].[Volumes] WHERE VolumePercentUsed >= '90'")


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
    for row in cursor:
        print(row)

main()

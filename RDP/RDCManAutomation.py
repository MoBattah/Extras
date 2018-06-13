import pyodbc

def main():
    cursor = SQLGET()
    createlists(cursor)
def createlists(cursor):
    for item in cursor:
        print(item[0])
        print(item[1])

def createstring():
    head = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    RDCManopen = "<RDCMan programVersion=\"2.7\" schemaVersion=\"3\"><file><credentialsProfiles /><properties><expanded>True</expanded><name>aformat</name></properties>"
    OperationsGroup = "<group><properties><expanded>True</expanded><name>Operations</name></properties><server><properties><name>mwm.vistex.com</name></properties></server><server><properties><name>NC01IISWSS004.hawkeyeww.com</name></properties></server></group>"
    DevGroup = "<group> <properties> <expanded>True</expanded> <name>Development</name> </properties> <server> <properties> <name>NC01IISWPS004.hawkeyeww.com</name> </properties> </server> </group>"
    ProdGroup = "<group> <properties> <expanded>True</expanded> <name>Production</name> </properties> <server> <properties> <name>nc01IISWPS005.hawkeyeww.com</name> </properties> </server> </group>"
    Ending = "</file> <connected /> <favorites /> <recentlyUsed /> </RDCMan>"

    fp = open("C:\\Users\\mo.battah\\hello.rdg", 'w+')
    fp.write(head + RDCManopen + OperationsGroup + DevGroup + ProdGroup + Ending)
    fp.close()



def SQLGET():
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=devops01.database.windows.net;'
        r'DATABASE=DevOpsDB;'
        r'TRUSTED_CONNECTION=Yes;'
    )
    cursor = conn.cursor()
    sqlstring = "SELECT [ReportDate],[EnvironmentName],[ServerType],[ServerName],[Comments] FROM [dbo].[Server]"
    cursor.execute(sqlstring)
    return cursor

if __name__ == "__main__":
    main()

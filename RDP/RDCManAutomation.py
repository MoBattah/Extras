import pyodbc

def main():
    cursor = SQLGET()
    global demo, development, stage, production, operations, preproduction, it
    demo, development, stage, production, operations, preproduction, it = ([] for i in range(7))
    demo, development, stage, production, operations, preproduction, it = createlist1(cursor)
    createstring(demo, development, stage, production, operations, preproduction, it)
    cursor = SQLGET()
    createlist2(cursor)

def createlist1(cursor):
    for item in cursor:
        globals()[item[1].lower()].append(item[3])
    return demo, development, stage, production, operations, preproduction, it

def createlist2(cursor):
    SQL, SAP, LIC, CTX, UTL, SYB, ADS, VBC = ([] for i in range(8))
    for item in cursor:
        SQL.append(item[2])
    SQL = list(set(SQL))
    for item in SQL:
        print(item + ",")


def createstring(demo, development, stage, production, operations, preproduction, it):
    head = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    RDCManopen = "<RDCMan programVersion=\"2.7\" schemaVersion=\"3\"><file><credentialsProfiles /><properties><expanded>True</expanded><name>Servers</name></properties>"
    OperationsGroup = "<group> <properties> <expanded>True</expanded> <name>Operations</name> </properties>"
    DevGroup = "<group> <properties> <expanded>True</expanded> <name>Development</name> </properties>"
    StageGroup = "<group> <properties> <expanded>True</expanded> <name>Stage</name> </properties>"
    ProdGroup = "<group> <properties> <expanded>True</expanded> <name>Production</name> </properties>"
    Ending = "</file> <connected /> <favorites /> <recentlyUsed /> </RDCMan>"
    PreProductionGroup = "<group> <properties> <expanded>True</expanded> <name>PreProduction</name> </properties>"
    ITGroup = "<group> <properties> <expanded>True</expanded> <name>IT</name> </properties>"
    DemoGroup = "<group> <properties> <expanded>True</expanded> <name>Demo</name> </properties>"
    development = list(set(development))
    demo = list(set(demo))
    stage = list(set(stage))
    production = list(set(production))
    operations = list(set(operations))
    it = list(set(it))
    preproduction = list(set(preproduction))



    for item in production:
        ProdGroup = ProdGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    ProdGroup = ProdGroup + "</group>"
    for item in development:
        DevGroup = DevGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    DevGroup = DevGroup + "</group>"
    for item in stage:
        StageGroup = StageGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    StageGroup = StageGroup + "</group>"
    for item in demo:
        DemoGroup = DemoGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    DemoGroup = DemoGroup + "</group>"
    for item in preproduction:
        PreProductionGroup = PreProductionGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    PreProductionGroup = PreProductionGroup + "</group>"
    for item in it:
        ITGroup = ITGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    ITGroup = ITGroup + "</group>"
    for item in operations:
        OperationsGroup = OperationsGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    OperationsGroup = OperationsGroup + "</group>"


    fp = open("C:\\Users\\mo.battah\\final.rdg", 'w+')
    fp.write(head + RDCManopen + ProdGroup + DevGroup + StageGroup + DemoGroup + PreProductionGroup + ITGroup + OperationsGroup + Ending)
    fp.close()



def SQLGET():
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=devops01.database.windows.net;'
        r'DATABASE=DevOpsDB;'
        r'TRUSTED_CONNECTION=Yes;'
    )
    cursor = conn.cursor()
    sqlstring = "SELECT  [EnvironmentName] ,[SvrEnvironment] ,[SvrGroup] ,[ServerName] FROM [dbo].[ServerSummary]"
    cursor.execute(sqlstring)
    return cursor

if __name__ == "__main__":
    main()

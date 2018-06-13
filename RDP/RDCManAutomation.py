import pyodbc

def main():
    cursor = SQLGET()
    global demo, development, stage, uncat, production, ops, integration, deprecated
    demo = []
    development = []
    integration = []
    production = []
    stage = []
    uncat = []
    ops = []
    deprecated = []
    demo, development, stage, uncat, production, ops, integration, deprecated = createlist(cursor)
    createstring(demo, development, stage, uncat, production, ops, integration, deprecated)

def createlist(cursor):
    switchstmt = {
        'Demo': lambda x: demo.append(x),
        'Development' : lambda x: development.append(x),
        'Stage': lambda x: stage.append(x),
        'Uncategorized': lambda x: uncat.append(x),
        'Production': lambda x: production.append(x),
        'Operations': lambda x: ops.append(x),
        'Integration': lambda x: integration.append(x),
        'DEPRECATED': lambda x: deprecated.append(x),
    }
    for item in cursor:
        switchstmt[item[1]](item[3])
    return demo, development, stage, uncat, production, ops, integration, deprecated

def createstring(demo, development, stage, uncat, production, ops, integration, deprecated):
    head = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    RDCManopen = "<RDCMan programVersion=\"2.7\" schemaVersion=\"3\"><file><credentialsProfiles /><properties><expanded>True</expanded><name>aformat</name></properties>"
    OperationsGroup = "<group> <properties> <expanded>True</expanded> <name>Operations</name> </properties>"
    DevGroup = "<group> <properties> <expanded>True</expanded> <name>Development</name> </properties>"
    StageGroup = "<group> <properties> <expanded>True</expanded> <name>Stage</name> </properties>"
    ProdGroup = "<group> <properties> <expanded>True</expanded> <name>Production</name> </properties>"
    DeprecatedGroup = "<group> <properties> <expanded>True</expanded> <name>DEPRECATED</name> </properties>"
    Ending = "</file> <connected /> <favorites /> <recentlyUsed /> </RDCMan>"
    UncatGroup = "<group> <properties> <expanded>True</expanded> <name>Uncategorized</name> </properties>"
    IntegrationGroup = "<group> <properties> <expanded>True</expanded> <name>Integration</name> </properties>"
    DemoGroup = "<group> <properties> <expanded>True</expanded> <name>Demo</name> </properties>"
    development = list(set(development))
    demo = list(set(demo))
    stage = list(set(stage))
    uncat = list(set(uncat))
    production = list(set(production))
    ops = list(set(ops))
    integration = list(set(integration))
    deprecated = list(set(deprecated))


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
    for item in uncat:
        UncatGroup = UncatGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    UncatGroup = UncatGroup + "</group>"
    for item in integration:
        IntegrationGroup = IntegrationGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    IntegrationGroup = IntegrationGroup + "</group>"
    for item in deprecated:
        DeprecatedGroup = DeprecatedGroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    DeprecatedGroup = DeprecatedGroup + "</group>"


    fp = open("C:\\Users\\mo.battah\\final.rdg", 'w+')
    fp.write(head + RDCManopen + DevGroup + StageGroup + ProdGroup + DemoGroup + UncatGroup + IntegrationGroup + DeprecatedGroup + Ending)
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

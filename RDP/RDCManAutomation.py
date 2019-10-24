#OBSOLETE, DO NOT USE
import pyodbc

def main():
    cursor = SQLGET()
    global demo, development, stage, production, operations, preproduction, it
    demo, development, stage, production, operations, preproduction, it = ([] for i in range(7))
    demo, development, stage, production, operations, preproduction, it = environmentlist(cursor)
    createstring(demo, development, stage, production, operations, preproduction, it)
    cursor = SQLGET()
    svrgrouplist(cursor)

def environmentlist(cursor):
    for item in cursor:
        globals()[item[1].lower()].append(item[3])
    return demo, development, stage, production, operations, preproduction, it

def svrgrouplist(cursor):
    global CFW, OSS, HBK, NAMESERVER, SVC, BOD, LVM, SOL, WEB, DOS, BLP, SVN, HDP, AFS, CMC, TRX, CSF, BQE, SEC, FIL, NPS, HDA, OFS, NPM, DEV, CTX, CTL, SBK, WHD, MRW, UCS, CMS, VFS, LIC, CNS, ESX,VSHIELDFW, IMG, VMWARETEMPLATE, DOC, ORA, SQl, CDC, BOB, FIN, PFS, GBK, SPE, SRM, ONE, UMT, SAP, SCS, UTL, HDC, PRS, FSS, SYB, OBK, VBR, VCS, SFS, WDS, SMT, DHP, OPS, FOG, RDP, SPT, TST, NOP, CAD, WDP, VBP, SGS, ADS, TFS, GIP, CPS, ECA, APP, CFS, DVM, VCP, OWA, KSN, DNS, HAN, SLG, RAD, CSQ, SUS, PDQ, QVA, ADC, SPECIALVM, FTP, BTI, CFP, TAB, TFB, VBC, SQL, DBK, VID, SPO, TEL, ASS, CSG
    CFW, OSS, HBK, NAMESERVER, SVC, BOD, LVM, SOL, WEB, DOS, BLP, SVN, HDP, AFS, CMC, TRX, CSF, BQE, SEC, FIL, NPS, HDA, OFS, NPM, DEV, CTX, CTL, SBK, WHD, MRW, UCS, CMS, VFS, LIC, CNS, ESX, VSHIELDFW, IMG, VMWARETEMPLATE, DOC, ORA, SQl, CDC, BOB, FIN, PFS, GBK, SPE, SRM, ONE, UMT, SAP, SCS, UTL, HDC, PRS, FSS, SYB, OBK, VBR, VCS, SFS, WDS, SMT, DHP, OPS, FOG, RDP, SPT, TST, NOP, CAD, WDP, VBP, SGS, ADS, TFS, GIP, CPS, ECA, APP, CFS, DVM, VCP, OWA, KSN, DNS, HAN, SLG, RAD, CSQ, SUS, PDQ, QVA, ADC, SPECIALVM, FTP, BTI, CFP, TAB, TFB, VBC, SQL, DBK, VID, SPO, TEL, ASS, CSG = ([] for i in range(109))
    for item in cursor:
        try: globals()[item[2].upper()].append(item[3])
        except KeyError:
            if item[2] == "VSHIELD-FW":
                VSHIELDFW.append(item[3])


def createstring(demo, development, stage, production, operations, preproduction, it):
    RDCManopen = "<?xml version=\"1.0\" encoding=\"utf-8\"?><RDCMan programVersion=\"2.7\" schemaVersion=\"3\"><file><credentialsProfiles /><properties><expanded>True</expanded><name>Servers</name></properties>"
    OperationsGroup = "<group> <properties> <expanded>True</expanded> <name>Operations</name> </properties>"
    DevGroup = "<group> <properties> <expanded>True</expanded> <name>Development</name> </properties>"
    StageGroup = "<group> <properties> <expanded>True</expanded> <name>Stage</name> </properties>"
    ProdGroup = "<group> <properties> <expanded>True</expanded> <name>Production</name> </properties>"
    Ending = "</file> <connected /> <favorites /> <recentlyUsed /> </RDCMan>"
    PreProductionGroup = "<group> <properties> <expanded>True</expanded> <name>PreProduction</name> </properties>"
    ITGroup = "<group> <properties> <expanded>True</expanded> <name>IT</name> </properties>"
    DemoGroup = "<group> <properties> <expanded>True</expanded> <name>Demo</name> </properties>"
    svrlist = demo, development, stage, production, operations, preproduction, it
    DemoGroup = groupstring(DemoGroup, demo)
    DevGroup = groupstring(DevGroup, development)
    StageGroup = groupstring(StageGroup, stage)
    ProdGroup = groupstring(ProdGroup, production)
    PreProductionGroup = groupstring(PreProductionGroup, preproduction)
    ITGroup = groupstring(ITGroup, it)
    OperationsGroup = groupstring(OperationsGroup, operations)
    grouplist = ProdGroup + DevGroup + StageGroup + DemoGroup + PreProductionGroup + ITGroup + OperationsGroup
    fp = open("C:\\Users\\mo.battah\\final.rdg", 'w+')
    fp.write(RDCManopen + grouplist + Ending)
    fp.close()


def groupstring(servgroup, servlist):
    servgroup = servgroup
    for item in servlist:
        servgroup = servgroup + "<server> <properties> <name>" + item + "</name> </properties> </server>"
    servgroup = servgroup + "</group>"
    return servgroup


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

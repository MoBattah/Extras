import pyodbc

def SQLGET():
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=devops01.database.windows.net;'
        r'DATABASE=DevOpsDB;'
        r'TRUSTED_CONNECTION=Yes;'
    )
    cursor = conn.cursor()
    sqlstring = "SELECT [ServerType] ,[SvrEnvironment] ,[SvrGroup] ,[ServerName] ,[Comments] ,[DataCenter] ,[Domain] ,[DatacenterName] ,[IPAddress] ,[OperatingSystem] ,[CPUCount] ,[MemoryInGB] ,[SumServerDiskSizeGB] ,[EstMonthlyCost] FROM [dbo].[ServerSummary]"
    cursor.execute(sqlstring)
    for item in cursor:
        print(item)
    return cursor

SQLGET()

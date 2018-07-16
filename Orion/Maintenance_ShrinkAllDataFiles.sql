USE msdb

CREATE TABLE #DBList (
	name varchar(1000),
	db_size varchar(300),
	owner varchar(300) null,
	dbid int,
	created datetime,
	status varchar(500),
	compatability_level int
)

INSERT INTO #DBList
EXEC sp_helpdb

DECLARE @DBID int
DECLARE @DBName varchar(300)
DECLARE @DataFileName varchar(300)
DECLARE @SQL varchar(2000)

DECLARE DB_Cursor CURSOR FOR 
SELECT dbid,
	name
FROM #DBList
--WHERE owner <> 'sa'
--WHERE name in ('foglight')
--WHERE name in ('msdb')
--WHERE name in ('PartnerWalletDB')
--WHERE name in ('HawkeyeReportingDB')
--WHERE name in ('distribution')
WHERE name not in ('master', 'model', 'msdb', 'tempdb', 'distribution', 'ReplicationDistribution')
            
OPEN DB_Cursor
FETCH NEXT FROM DB_Cursor INTO @DBID, @DBName

WHILE @@FETCH_STATUS = 0
BEGIN
	PRINT @DBName

	--Assumes single log file presently, may need cursor
	SELECT @DataFileName = name
	FROM sys.master_files
	WHERE database_id = @DBID
	AND type_desc = 'ROWS'

	PRINT @DataFileName
	SET @SQL = 'USE [' + @DBName + ']; DBCC SHRINKFILE ([' + @DataFileName + '], 10) WITH NO_INFOMSGS'
	EXEC(@SQL)

	FETCH NEXT FROM DB_Cursor INTO @DBID, @DBName
END

CLOSE DB_Cursor
DEALLOCATE DB_Cursor

DROP TABLE #DBList
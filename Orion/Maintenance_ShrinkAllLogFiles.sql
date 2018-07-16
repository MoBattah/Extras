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
DECLARE @LogFileName varchar(300)
DECLARE @SQL varchar(2000)

DECLARE DB_Cursor CURSOR FOR 
SELECT dbid,
	name
FROM #DBList

WHERE name not in ('master', 'model', 'msdb', 'tempdb', 'distribution', 'ReplicationDistribution')
            
OPEN DB_Cursor
FETCH NEXT FROM DB_Cursor INTO @DBID, @DBName

WHILE @@FETCH_STATUS = 0
BEGIN
	PRINT @DBName

	--Assumes single log file presently, may need cursor
	SELECT @LogFileName = name
	FROM sys.master_files
	WHERE database_id = @DBID
	AND type_desc = 'LOG'

	PRINT @LogFileName
	SET @SQL = 'USE [master]; ALTER DATABASE [' + @DBName + '] SET RECOVERY SIMPLE WITH NO_WAIT'
	EXEC(@SQL)
	SET @SQL = 'USE [' + @DBName + ']; DBCC SHRINKFILE ([' + @LogFileName + '], 10) WITH NO_INFOMSGS'
	EXEC(@SQL)
	SET @SQL = 'USE [master]; ALTER DATABASE [' + @DBName + '] SET RECOVERY FULL WITH NO_WAIT'
	EXEC(@SQL)

	FETCH NEXT FROM DB_Cursor INTO @DBID, @DBName
END

CLOSE DB_Cursor
DEALLOCATE DB_Cursor

DROP TABLE #DBList

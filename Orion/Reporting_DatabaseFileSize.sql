SELECT DISTINCT UPPER(volume_mount_point) as volume_mount_point,
	(total_bytes/1048576) as total_mb,
	(total_bytes/1073741824) as total_gb,
	(available_bytes/1048576) as available_mb,
	(available_bytes/1073741824) as available_gb,
	(((available_bytes/1048576.0)/(total_bytes/1048576.0))*100.0) as pct_free
FROM sys.master_files AS f  
	CROSS APPLY sys.dm_os_volume_stats(f.database_id, f.file_id)
ORDER BY volume_mount_point

CREATE TABLE #MDFFileInformation (
	ServerName VARCHAR(100) NOT NULL,
	DatabaseName VARCHAR(100) NOT NULL,
	LogicalFileName SYSNAME NOT NULL,
	PhysicalFileName NVARCHAR(520),
	Status SYSNAME,
	RecoveryMode SYSNAME,
	FileSizeMB INT,
	FreeSpaceMB INT,
	FreeSpacePct INT,
	DateAndTime VARCHAR(10) NOT NULL
)

ALTER TABLE #MDFFileInformation ADD CONSTRAINT Comb_SNDNDT2_MDF UNIQUE(ServerName, DatabaseName, Dateandtime, LogicalFileName)
ALTER TABLE #MDFFileInformation ADD CONSTRAINT Pk_SNDNDT2_MDF PRIMARY KEY (ServerName, DatabaseName, Dateandtime, LogicalFileName)

DECLARE @CommandGetMDFDetail VARCHAR(5000)
SELECT @CommandGetMDFDetail = '
	USE [' + '?' + ']
	SELECT @@SERVERNAME as ServerName,
		' + '''' + '?' + '''' + ' AS DatabaseName,
		sysfiles.name AS LogicalFileName,
		sysfiles.filename AS PhysicalFileName,
		CONVERT(sysname,DatabasePropertyEx(''?'',''Status'')) AS Status,
		CONVERT(sysname,DatabasePropertyEx(''?'',''Recovery'')) AS RecoveryMode,
		CONVERT(int,((size*8.0)/1024.0)) as FileSizeMB,
		CONVERT(int,(((size*8.0) - (FILEPROPERTY(name, ' + '''' + 'SpaceUsed' + '''' + ' )*8.0))/1024.0)) as FreeSpaceMB,
		CONVERT(int,(100.0*(((size*8.0) - (FILEPROPERTY(name, ' + '''' + 'SpaceUsed' + '''' + ' )*8.0))/1024.0)/((size*8.0)/1024.0))) as FreeSpacePct,
		CONVERT(VARCHAR(10),GETDATE(),111) as DateAndTime
	FROM dbo.sysfiles
	WHERE sysfiles.filename LIKE ''%mdf''
'

INSERT INTO #MDFFileInformation (
	ServerName,
	DatabaseName,
	LogicalFileName,
	PhysicalFileName,
	Status,
	RecoveryMode,
	FileSizeMB,
	FreeSpaceMB,
	FreeSpacePct,
	DateAndTime
)
EXEC sp_MSForEachDB @CommandGetMDFDetail

CREATE TABLE #LDFFileInformation (
	ServerName VARCHAR(100) NOT NULL,
	DatabaseName VARCHAR(100) NOT NULL,
	LogicalFileName SYSNAME NOT NULL,
	PhysicalFileName NVARCHAR(520),
	Status SYSNAME,
	RecoveryMode SYSNAME,
	FileSizeMB INT,
	FreeSpaceMB INT,
	FreeSpacePct INT,
	Dateandtime VARCHAR(10) NOT NULL
)

ALTER TABLE #LDFFileInformation ADD CONSTRAINT Comb_SNDNDT2_LDF UNIQUE(ServerName, DatabaseName, Dateandtime, LogicalFileName)
ALTER TABLE #LDFFileInformation ADD CONSTRAINT Pk_SNDNDT2_LDF PRIMARY KEY (ServerName, DatabaseName, Dateandtime, LogicalFileName)

DECLARE @CommandGetLDFDetail VARCHAR(5000)
SELECT @CommandGetLDFDetail = '
	USE [' + '?' + ']
	SELECT @@SERVERNAME as ServerName,
		' + '''' + '?' + '''' + ' AS DatabaseName,
		sysfiles.name AS LogicalFileName,
		sysfiles.filename AS PhysicalFileName,
		CONVERT(sysname,DatabasePropertyEx(''?'',''Status'')) AS Status,
		CONVERT(sysname,DatabasePropertyEx(''?'',''Recovery'')) AS RecoveryMode,
		CONVERT(int,((size*8.0)/1024.0)) as FileSizeMB,
		CONVERT(int,(((size*8.0) - (FILEPROPERTY(name, ' + '''' + 'SpaceUsed' + '''' + ' )*8.0))/1024.0)) as FreeSpaceMB,
		CONVERT(int,(100.0*(((size*8.0) - (FILEPROPERTY(name, ' + '''' + 'SpaceUsed' + '''' + ' )*8.0))/1024.0)/((size*8.0)/1024.0))) as FreeSpacePct,
		CONVERT(VARCHAR(10),GETDATE(),111) as DateAndTime
	FROM dbo.sysfiles
	WHERE sysfiles.filename LIKE ''%ldf''
'

INSERT INTO #LDFFileInformation (
	ServerName,
	DatabaseName,
	LogicalFileName,
	PhysicalFileName,
	Status,
	RecoveryMode,
	FileSizeMB,
	FreeSpaceMB,
	FreeSpacePct,
	DateAndTime
)
EXEC sp_MSForEachDB @CommandGetLDFDetail

--select * from #MDFFileInformation
--select * from #LDFFileInformation

select #MDFFileInformation.ServerName, 
       #MDFFileInformation.DatabaseName,
	   #MDFFileInformation.LogicalFileName,
	   left(#MDFFIleInformation.PhysicalFileName, 1) as DiskLabel,
	   #MDFFileInformation.PhysicalFileName,
       #MDFFileInformation.Status, 
       #MDFFileInformation.RecoveryMode as RecoveryModel, 
       #MDFFileInformation.filesizemb as FilesizeMB, 
       #MDFFileInformation.FreeSpaceMB as FreeSpaceMB, 
       case
		when #MDFFileInformation.filesizemb = 0 then 100
		else #MDFFileInformation.FreeSpacePct
       end as FreeSpacePct
from #MDFFileInformation
where #MDFFileInformation.databasename not in ('master', 'model', 'msdb', 'tempdb', 'distribution', 'ReplicationDistribution')
union
select #LDFFileInformation.ServerName, 
       #LDFFileInformation.DatabaseName,
	   #LDFFileInformation.LogicalFileName,
	   left(#LDFFIleInformation.PhysicalFileName, 1) as DiskLabel,
	   #LDFFileInformation.PhysicalFileName,
       #LDFFileInformation.Status, 
       #LDFFileInformation.RecoveryMode as RecoveryModel, 
       #LDFFileInformation.filesizemb as FilesizeMB, 
       #LDFFileInformation.FreeSpaceMB as FreeSpaceMB, 
       case
		when #LDFFileInformation.filesizemb = 0 then 100
		else #LDFFileInformation.FreeSpacePct
       end as FreeSpacePct
from #LDFFileInformation
where #LDFFileInformation.databasename not in ('master', 'model', 'msdb', 'tempdb', 'distribution', 'ReplicationDistribution')
--order by DatabaseName asc
order by DiskLabel desc,
	FreeSpaceMB desc

DROP TABLE #MDFFileInformation
DROP TABLE #LDFFileInformation
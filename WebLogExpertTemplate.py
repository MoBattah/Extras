from jinja2 import Template
import pyodbc
import os

def main():
    SQLList = SQLGET()
    profileList = FetchProfileFolder()
    CompareData(profileList, SQLList)
def SQLGET():
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=devops01test.database.windows.net;'
        r'DATABASE=TestWebHookDB;'
        r'UID=user;'
        r'PWD=pass'
    )
    cursor = conn.cursor()
    sqlstring = "SELECT TOP (1000) [ProfileName],[ProfileType],[LogFilePath],[TargetFilePath] FROM [dbo].[profiles]"
    cursor.execute(sqlstring)
    return cursor


def FetchProfileFolder():
    url = "C:\\Users\\mo.battah\\Documents\\WebLog\\Profiles" #where profiles are located
    profileList = os.listdir(path=url)
    return profileList

def CreateTemplate():
    t = Template("[Profile]\nName={{PName}}\n[General]\nIndexFile=default.aspx\nDomain={{domain}}\nDNSLookup=1\n"\
             "bRetrievePageTitles=0\nbUseANalysisCache=1\nPaidSearchAndGoals=0\nCustomAnalysisSettings=0\n"\
             "AnalysisSettings-iShowFileQueryParameters=0\nAnalysisSettings-stFileQueryParameters=\n"
             "AnalysisSettings-iFileNamesCase=0\nAnalysisSettings-bConvertFileQueriesToLowerCase=0\n"
             "AnalysisSettings-fTimeOffset=0.000\nAnalysisSettings-iTimeZone=0\nAnalysisSettings-iDateFormat=0\n"
             "AnalysisSettings-iFirstDayOfWeek=0\nAnalysisSettings-stDateFormat=mm/dd/yyyy\nAnalysisSettings-iHostsReport\n"
             "AnalysisSettings-iCOuntSpidersAsVistors=0\n[Logs]\nSource=0\nFilePath={{logfilepath}}\n"
             "LogFormat-Format=0\nUseTrackingCode=0\n[LandingPages]\nCount=0\n[ConversionGoals]\n"
             "Count=0\n[TimeRange]\nType=0\nPeriodCount=2\nStartTime=1301616000\nEndTime=1304207999"
             "\nbMultipleTimeRangeHTMLReports=0\n[Tracking]\nCount=0\n[Filters]\nCount=6\nFilterType0=1\n"
             "FilterCriteria0=0\nFilter0=5\nMask0=*nagios*\nCaseSensitive0=0\nIncludeQuery0=0\nIncludeVersion0=0\n"
             "SearchResultType0=0\nEnabled0=1\nFilterType1=1\nFilterCriteria1=0\nFilter1=5\n"
             "Mask1=*pingdom*\nCaseSensitive1=0\nIncludeQuery1=0\nIncludeVersion1=0\nSearchResultType1=0"
             "\nEnabled1=1\nFilterType2=1\nFilterCriteria2=0\nFilter2=0\nMask2=*nagios*\nCaseSensitive2=0\n"
             "IncludeQuery2=0\nIncludeVersion2=0\nSearchResultType2=0\nEnabled2=1\nFilterType3=1\n"
             "FilterCriteria3=0\nFilter3=0\nMask3=*pingdom*\nCaseSensitive3=0\nIncludeQuery3=0\n"
             "IncludeVersion3=0\nSearchResultType3=0\nEnabled3=1\nFilterType4=1\nFilterCriteria4=0\n"
             "Filter4=0\nMask4=clt1-wwb01.hawkeyeww.com\nCaseSensitive4=0\nIncludeQuery4=0\n"
             "IncludeVersion4=0\nSearchResultType4=0\nEnabled4=1\nFilterType5=1\nFilterCriteria5=0\n"
             "Filter5=15\nMask5=*\nCaseSensitive5=0\nIncludeQuery5=0\nIncludeVersion5=0\n"
             "SearchResultType5=0\nEnabled5=1\n[Report]\nDest=4\nServerUsers=\nCustomDashboardSettings=0"
             "\nSaveRawData=1\nCustomCommonReportFormat=0\nReportFormat=1\nCustomPDFReportFormat=0"
             "\nCustomReportContents=0\nReplaceDailyChart=0\nShowReport=0")
    ProfileName=""
    Domain=""
    LogFilePath=""
    apfl = t.render(PName=ProfileName,domain=Domain,logfilepath=LogFilePath)
    print(apfl)


    with open("newfile.pfl", "w") as fh:
        fh.write(apfl)
        fh.close()

def CompareData(profileList, SQLList):
    profileNames = []
    for row in SQLList:
        profileNames.append(row[0])  #creating a profileNames list of the profile names from SQL
    url2 = "C:\\Users\\mo.battah\\Documents\\WebLog\\Profiles\\" #url2 keeps the last two slashes
    count = 0
    domainlist = []
    for item in profileList:
        xpath = url2 + profileList[count]
        fp = open(xpath, 'r')
        line = fp.readlines()
        line = line[1] #grabs name= line
        domainname = str(line[5:len(line)-1])
        domainlist.append(domainname)
        count = count + 1
    #print(domainlist)
    a = set(domainlist) & set(profileNames)
    print(a)
    print("length of a: ", len(a))
    print("length of domain list: ", len(domainlist))
    print("length of profilenames: ", len(profileNames))


if __name__ == "__main__":
    main()



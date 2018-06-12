from jinja2 import Template
import pyodbc
import os
import sys
from shutil import copyfile
import datetime

def main():
    global url #Profiles location
    global url2 #Profiles location with slashes
    global url3 # Text file
    url = "C:\\ProgramData\\WebLog Expert\\Profiles"  #type in here where your profiles are located
    url2 = url + "\\"
    url3 = "E:\\Web\\WebLogExpertAutomation\\BatList.txt"  #Type in where the ProfilesList text file should be located for the nightly batch file run
    if os.path.exists(url + "\\logfile.txt"):   #LOGGING
        sys.stdout = open(url + "\\logfile.txt", 'a+')
    else:
        sys.stdout = open(url + "\\logfile.txt", "w+")
    print("Start: ", str(datetime.datetime.now()).split('.')[0])
    chkmkdirs()
    try:
        if sys.argv[1] == 'r': #if r is passed as an argument, run the renamer script
            renameDIGITFiles()
    except:
        print("No arguments passed. Will not run renamer script.")
    SQLList = SQLGET()
    profileList = FetchProfileFolder()
    WebProfilesToBeAdded, DomainNamesToBeAdded, LogPaths = CompareData(profileList, SQLList)
    count = 0
    for x, y, z in zip(WebProfilesToBeAdded, DomainNamesToBeAdded, LogPaths):
        profile = WebProfilesToBeAdded[count]
        domain = DomainNamesToBeAdded[count]
        logpath = LogPaths[count]
        CreateTemplate(profile, domain, logpath)
        count = count + 1
    updatetextfile()
    print("End: ", str(datetime.datetime.now()).split('.')[0])

    sys.stdout.close()  ###LOGGING
def SQLGET():
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=devops01test.database.windows.net;'
        r'DATABASE=TestWebHookDB;'
        r'UID=;'
        r'PWD='
    )
    cursor = conn.cursor()
    sqlstring = "SELECT TOP (1000) [ProfileName],[ProfileType],[LogFilePath],[TargetFilePath] FROM [dbo].[profiles]"
    cursor.execute(sqlstring)
    return cursor


def FetchProfileFolder():
    profileList = []
    directorylist = os.listdir(path=url)
    for item in directorylist:
        if os.path.isfile(url2 + item):
            profileList.append(item)
        else: print(item, " is a directory and not a file.")
    return profileList

def CreateTemplate(ProfileName, Domain, LogFilepath):
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
    TProfileName=ProfileName
    TDomain = Domain
    TLogFilePath=LogFilepath
    apfl = t.render(PName=TProfileName,domain=TDomain,logfilepath=TLogFilePath)
    NewProfilePath = url + "\\NewProfiles\\"
    filename = NewProfilePath + TProfileName + ".pfl"
    with open(filename, "w") as fh:
        fh.write(apfl)
        fh.close()


def CompareData(profileList, SQLList):
    SQLprofileNames = []
    LogPaths = []
    for row in SQLList:
        if row[1] == "Web": #taking out any PDF profiles
            SQLprofileNames.append(row[0])  #creating a SQLprofileNames list of the profile names from SQL DB
            LogPaths.append(row[2]) #creating LogPaths list of log paths from SQL DB
    count = 0
    OSdomainlist = []
    for item in profileList:  #This loop will look through what files the OS has and it will make a list of the files based upon their profile name...profile name so that it matches up with the SQL name column.
        xpath = url2 + profileList[count]
        fp = open(xpath, 'r')
        line = fp.readlines()
        line = line[1] #grabs name= line
        domainname = str(line[5:len(line)-1])
        OSdomainlist.append(domainname)
        count = count + 1
    overlap = set(OSdomainlist) & set(SQLprofileNames)
    print("These ", len(overlap), " profiles are already in WebLogExpert: \n", overlap)
    toBeAddedProfiles = set(SQLprofileNames) - set(OSdomainlist)
    toBeAddedProfiles = list(toBeAddedProfiles) #converting from set to list
    print("\nThese", len(toBeAddedProfiles),"profiles are not in WebLogExpert but they should be: \n", toBeAddedProfiles)
    domainnames = []
    for item in toBeAddedProfiles: #getting domain names
        line = item[item.index('_') + 1:len(item)]  #find where the underscore starts and only take what's after it, the actual domain names
        domainnames.append(line)
    return toBeAddedProfiles, domainnames, LogPaths

def renameDIGITFiles():
    profileList = os.listdir(path=url) #checks whats in the directory
    print("List of files in ", url, profileList)

    for item in profileList:
        fname = item[0:len(item) - 4]  # getting the filename without extension
        if fname.isdigit() == True:  # comparing that to an integer to see if needs be copied/renamed
            fp = open(url2 + item, 'r')  # opens pfl file and reads
            line = fp.readlines()
            print(line[1])
            line = line[1]  # Gets the Name= line
            profileName = str(line[5:len(line) - 1]) #cuts off name= part
            print(profileName)
            namesource = url2 + fname + ".pfl"
            print("Renaming from ", namesource)
            namedest = profileName + fname + ".pfl"  # add fname to avoid same domain
            namedest = namedest.replace('\\', '_') #filter out slahes and stars from destination filename
            namedest = namedest.replace('/', '_')
            namedest = namedest.replace('*', '_')
            namedest = url2 + namedest
            print(namesource)
            print("Renamed to ", namedest)
            try:
                copyfile(namesource, namedest)
            except FileNotFoundError:
                print("This will need a check: " + namedest)
        else:
            print("please check " + item)

def chkmkdirs():
    if not os.path.exists(url2 + "NewProfiles\\"):
        os.makedirs(url2 + "NewProfiles\\")
        print("Created NewProfiles folder in ", url2)
    if not os.path.exists(url2 + "RenamedProfiles\\"):
        os.makedirs(url2 + "RenamedProfiles\\")
        print("Created RenamedProfiles folder in ", url2 + "RenamedProfiles\\")


def updatetextfile():
    SQLList = SQLGET()
    SQLProfileNames = []
    for row in SQLList:
        SQLProfileNames.append(row[0])  #creating a SQLProfileNames list of the profile names from SQL DB
    textfile = open(url3, 'r+')
    textfile.truncate()
    for item in SQLProfileNames:
        textfile.write(item + '\n')
    print("Updated profile list text file. ")


if __name__ == "__main__":
    main()



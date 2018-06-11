import os

for x in range(1,1674):
    counter = str(x)
    astring = "BCP \'SELECT TOP (1) [FileContent] FROM [Recruitment].[dbo].[file_docx_vw] WHERE [ID] = " + counter + "' queryout C:\\Users\\mo.battah\\Documents\\resume"+ counter + ".docx -n -T  -S defrsqlwp005.vistex.local"
    astring = str(astring)
    print(astring)
    os.system('powershell.exe ' + astring)


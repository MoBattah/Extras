import os
astring = "BCP \'SELECT TOP (1) [FileContent] FROM [Recruitment].[dbo].[file_docx_vw] WHERE [ID] = 72' queryout C:\\Users\\mo.battah\\Documents\\filey2.docx -n -T  -S defrsqlwp005.vistex.local"
os.system('powershell.exe ' + astring)

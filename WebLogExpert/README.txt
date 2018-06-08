WebLogExpert Engine
-------------------------

This application is designed to automate and maintain a Web Log Expert installation. 

Use:
Launched with the required packages installed: `python WebLogExpertEngine.py`
If you'd like your files renamed to their correct profile names, add 'r' as an option: `python WebLogExpertEngine.py r`

The application will correctly rename WebLogExpert Profile files based upon their profile name as shown in the GUI. Then the application will fetch two lists - 
1. The list of profiles that should be in WebLogExpert via SQL server.
2. The list of profiles currently in your WebLogExpert installation.
These two lists will be compared and any profiles not in your installation, will be created automatically and placed into a folder named 'NewProfiles'. *you can customize this by editing the code.

All changes made are logged to a logfile from where you launched the script. 

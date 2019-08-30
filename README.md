# LSSS utilities
Python library for adding utilities in  LSSS. This is collection of smaller features that we created and have made available. They can be used as is, or used as templates for your own functions.

## Initialisation
To enable the functionality in LSSS follow these steps
1. Go to "LSSS configuration" and change to "Adminstrator mode"
2. Turn on the incubator feature in LSSS. This requires adding `-Dno.marec.incubator=true` to the JAVA_OPTS environment variable. There are two ways to do this:
    * Adding `"-Dno.marec.incubator=true"^` in the  `\Marec\LSSS 2.6.0\lsss\LSSS.bat` file, under the block starting with `"%JAVA%" %JAVA_OPTS%` above the `no.imr.lsss.main.LsssMain %*` line (every time you install/upgrade LSSS you will have to do this again), OR
    * Setting the variable via the operating system. The procedure varies with your operating system and version. For Windows 10, open the Control Panel, choose 'User Accounts', then 'Change my environment variables', then edit the JAVA_OPTS variable to include `-Dno.marec.incubator=true`. If there are already items in that variable, separate them with a semicolon.
    * Restart LSSS
3. Go to "LSSS configuration" -> "Application configuration" -> "Plugins" and tick "LSSS server" & "LSSS incubator"
3. Restart LSSS
4. Go to "LSSS configuration" -> "Application configuration" -> "Miscellaneous" -> "LSSS server" and tick "Start LSSS scritping server"
5. Test that the server is running by clicking on "Open web page". Here you will also find the API documentation.

## Installation 
1. Download zip file of the repository (https://github.com/nilsolav/LSSS_utilities/archive/master.zip)
1. Install it using the "LSSS configuration" -> "Application configuration" -> "Packages" dialog and choose to install from a zip file. The package will be installed under your user directory `\.ApplicationData\lsss\config\packagesConfig\packages\LSSS_utilities-master`.
1. IMPORTANT: The installer place the file under the subfolder `LSSS_utilities`. You need to copy the python files one directory level up. This wil be fixed in future versions.
1. Associate actions in the package with menu items, key-presses, or toolbar buttons
1. Enjoy

# Actions
## Demo 1
1. Demo1 (shows a dialog box that gives the duration of the visible pelagic echogram)
Dependencies
   1. `tkinter`
   1. `humanfriendly`

## Impor Add schools from external interpretation masks
TBA

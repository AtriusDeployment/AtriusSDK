# Introduction 
This early release Python 3 SDK is intended to enable retail ECLYPSE customers to complete several administrative tasks at fleet scale.
The example scripts should be executed in your OS terminal. Input is provided as command line parameters, output will be displayed in the terminal.
Scripts that deploy firmware require additional arguments.

# Getting Started
How to install this package:
1.	Unzip the package
2.	Install dependencies
>`pip install -r requirements.txt`
3.  Create an input csv file based on the provided example
4.  Copy an ECLYPSE firmware package zip file to the same directory
5.  Execute the script
>`python eclypse_firmware_upgrade.py host_list.csv eclypse_firmware.zip firmware_version`

# Input
Each script completes 1 task on multiple ECLYPSE controllers. A list of ECLYPSE controllers is supplied in a csv file with the following columns:
>hostname or ip address,username,password
For example, a file with a single ECLYPSE might contain: 
>192.168.1.2,admin,password

# Output
All output is displayed in the OS terminal following the executed command. 

# SSL Warning
The ECLYPSE UI and API enforce HTTPS by default with a default hostname and a self-signed certificate. The example scripts in this package bypass external
certificate verification using the verify option in the requests package. 
> `session.verify = False`

Which means you will receive this warning in the script output. 
> 1045: InsecureRequestWarning: Unverified HTTPS request is being made to host '192.168.1.4'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  warnings.warn

ECLYPSE supports replacing the self-signed certificate with one issued by a CA. That is beyond the scope of this SDK. 
If you wish to continue using the self signed certificate and suppress the warning, change SUPPRESS_SSL_WARNING at the top of each script to True.
> `SUPPRESS_SSL_WARNING = True`

# Execution
This is a flat Python package. Input files should be created in the same directory as the Python script. This should be the current directory when executing the scripts. 

Example: 
> `cd Downloads\AtriusClientSDK`

> `python eclypse_firmware_upgrade.py example_host_list.csv ECYSeries_v1.17.21196.747.zip 1.17.21196.747`

> `python eclypse_firmware_version.py example_host_list.csv`

# ECLYPSE Firmware Upgrades
The firmware upgrade script sends the upgrade zip file from Distech-Controls to every ECLYPSE in the csv file. 
The upgrade script indicates a successful upload with this message on the terminal: 
> {'host': '192.168.1.4', 'status': 'Complete - Uploaded 1.18.22259.846'}

A this point, the target ECLYPSE controller will verify the zip file and reboot to load the new firmware. The upgrade script will complete returning to a terminal prompt. 
Run the eclypse_firmware_version script to verify that all ECLYPSE are now running the new firmware. 
If the report indicates that some ELCYPSE are still running old firmware, run the upgrade script again. It will skip any ECLYPSE that are already upgraded. 

# Files Included
- eclypse.py - Python module includes functions to enable/disable interfaces, set timezone, upgrade firmware
- eclypse_firmware_upgrade.py - Python script to deploy ECLYPSE firmware at scale
- eclypse_firmware_version.py - Create a report of current firmware versions
- util.py - CLI input/output functions
- example_host_list.csv - Demonstrates the format for the required ECLYPSE list

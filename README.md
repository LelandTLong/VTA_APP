# VTA_APP
## Install and Setup Directions
1. This project uses python and mysql for main functionality, and uses flask for the server.
2. install python dependencies: argparse, requests, json, mysql-connector-python, Flask into Python\
`pip install {module}`\
or\
`python -m pip install {module}`
3. create key.py file in root directory by copying the format of the keys_template.py file\
user and password is for mysql DB credentials, API key is the one provided for the project
4. install MySQL web-community version with default setup: 'https://dev.mysql.com/downloads/installer/'.
5. start MySQL server
6. Run app: `python main.py --help` for all options\
`-c` flag deletes any and all data from the DB before getting the trip feed\
`-d` flag is the EC function to delete any expired TripUpdates if a new one comes in\
By default both flags are false if not provided.\
The app will create a DB called 'VTADatabase' and its tables automatically when needed.
7. Run server: `python server.py`. The endpoint will be 'http://localhost:5000/real-time/trip-updates'.

## Functionality:
All base functionality for project guidelines is complete\
EC done: ignore existing and append new tripupdates, delete outdated tripupdates\

## STRY Naming and Meaning
**STRY00000001**: Create base template\
**STRY00000002**: Parse API data and store into SQL DB\
**STRY00000003**: Create Server\
**STRY00000004**: Commandline features, cleaned DB design, and added deleting outdated tripupdates\
**STRY00000005**: Added removing outdated TripUpdates option\

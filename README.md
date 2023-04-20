# VTA_APP
## Install and Setup Directions
This project uses python and mysql for main functionality, and uses flask for the server.\
install modules: argparse, requests, json, mysql.connector, Flask into Python\
`pip install {module}`\
create key.py file in root directory copying the format of the template\
user and password is for mysql DB credentials, API key is the one provided for the project\
install MySQL with default setup\
start MySQL server\
Run app: `python main.py --help` for all options\
`-c` flag deletes any and all data from the DB before getting the trip feed\
`-d` flag is the EC function to delete any expired TripUpdates if a new one comes in\
Run server: `python server.py`. The endpoint will be 'http://localhost:5000/real-time/trip-updates'.\\

## Functionality:\
All base functionality for project guidelines is complete\
EC done: ignore existing and append new tripupdates, delete outdated tripupdates\\

## STRY Naming and Meaning
**STRY00000001**: Create base template\
**STRY00000002**: Parse API data and store into SQL DB\
**STRY00000003**: Create Server\
**STRY00000004**: Commandline features, cleaned DB design, and added deleting outdated tripupdates\
**STRY00000005**: Added removing outdated TripUpdates option\
**STRY00000006**: Prepare project and README instructions for submission\

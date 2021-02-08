# Final-project-Warehouse
Warehouse on MongoDB, client-server. Client has GUI.
# **Requirement**
## **MongoDB:**
### **Windows:**
https://medium.com/@LondonAppBrewery/how-to-download-install-mongodb-on-windows-4ee4b3493514
### **Linux:**
sudo apt-get install mongodb
### **MacOS:**
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/
## **Libraries:**
*   mongoengine
*   PySimpleGUI
*   socket
*   json
*   datetime
*   argparse
*   sys
*   configparser
# **Stucture of configDB.ini**
*   connection
*   mongo
# **Start**
run server:
```
main.py -t server
```
run client:
```
main.py -t client
```
## **First start**
First start fill empty database:

  users:

    Administrator
        login: admin
        password: admin

    Worker
        login: worker
        password: worker

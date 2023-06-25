#!/bin/bash

action=cp


#common
sed -i "s/cron = 0/cron = 1/g" backup.testnew.py
sed -i "s/action = 'null'/action = '$action'/g" backup.testnew.py
sed -i "s/database_type = 0/database_type = 3/g" backup.testnew.py

#For mysql
python3  python_script.py username passsword dbname dumpfile 

#For Mongo
python3  python_script.py dbname username password dumpfile

#For Postgres
python3  python_script.py dbname dumpfile


#common
sed -i "s/database_type = 3/database_type = 0/g" backup.testnew.py
sed -i "s/action = '$action'/action = 'null'/g" backup.testnew.py
sed -i "s/cron = 1/cron = 0/g" backup.testnew.py

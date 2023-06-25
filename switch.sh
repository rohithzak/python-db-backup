#!/bin/bash

action=<Enter your action> # cp, scp, s3

#common
sed -i "s/cron = 0/cron = 1/g" <python script>
sed -i "s/action = 'null'/action = '$action'/g" <python sscript>
sed -i "s/database_type = 0/database_type = 3/g" <python script>   # 1 -postgres, 2-Mysql, 3-Mongo

#For mysql
python3  <python script> username passsword dbname dumpfile 

#For Mongo
python3  <python script> dbname username password dumpfile

#For Postgres
python3 <python script> dbname dumpfile


#common
sed -i "s/database_type = 3/database_type = 0/g" <python script>    #input same value in which you gave above for database type
sed -i "s/action = '$action'/action = 'null'/g" <python script>
sed -i "s/cron = 1/cron = 0/g" <python script>

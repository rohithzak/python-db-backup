# python-db-backup

The script is designed to perform database backups and perform additional actions based on user input or command-line arguments. It utilizes various command-line tools and libraries to execute the backup and transfer operations.

Here's a breakdown of the script's functionality:

1.Importing required modules:

os: Provides a way to interact with the operating system, execute commands, and handle file operations.
sys: Provides access to system-specific parameters and functions.
smtplib: Enables sending emails using the Simple Mail Transfer Protocol (SMTP).
dotenv: Loads environment variables from a .env file into the script's environment.

2.Loading environment variables:

The script uses the dotenv module to load environment variables from a .env file. These variables store sensitive information such as email credentials and file paths.
3.Functions for database backups:

The script defines three functions to create backups for different database types: create_pg_dump, create_mysqldump, and create_mongodump. These functions use command-line tools (pg_dump, mysqldump, mongodump) to perform the backups.

4.Function for pushing files to S3:

The s3_push function takes a source file and uploads it to Amazon S3 using the AWS CLI (aws s3 cp command). It requires the user to specify the AWS profile and S3 URL.

5.Function for copying files:

The cp_file function copies a source file or directory to a destination using the cp command.

6.Function for transferring files via SCP:

The scp_file function transfers a file from the local machine to a remote server using the Secure Copy (SCP) protocol. It requires the user to provide the necessary parameters such as the private key file, source file, destination server details (username, IP address), and destination path.

7.Function for sending email notifications:

The send_email function uses the smtplib module to send email notifications. It requires the sender's email, receiver's email(s), and email credentials (sender email and password) as environment variables.

8.Main script logic:

The script contains a conditional block that checks the value of the cron variable. If cron is set to 0, it executes the backup and additional action based on user input.
If cron is not 0 (assumed to be non-zero), it assumes the script is being executed with command-line arguments. It extracts the necessary arguments (arg1, arg2, etc.) and performs the backup and additional action accordingly.

9.User input section:

When cron is 0, the script prompts the user to enter the database type (PostgreSQL, MySQL, MongoDB) and other required details for the backup operation.
It also prompts for the desired action (S3, SCP, or CP) to be performed after the backup.

10.Action execution based on user input:

Depending on the user's input, the script executes the corresponding action after the backup: S3 upload, SCP transfer, or local file copy.
Action execution based on command-line arguments:
When cron is not 0, the script assumes it's being executed with command-line arguments. It extracts the necessary arguments and performs the backup and additional action based on those arguments.
Email notifications:
After each action, the script sends email notifications indicating whether the backup or file transfer was successful or not. It uses the send_email function to send the emails.

We can use this pythons script to work automatically and manually too. If you want to use the script manually just run the script from your CLI and just input the neccessary inputs required and everything will br done by the script.
If you want to use this automatically you can set this as a cron and run it in a scheduled manner. For that I have added a bash script "switch.sh" in the repository which kinds of acts as a switch for the script.
There is a variable in the bash script with name action, specify the action you need to perfrorm for the action variable(cp, scp, s3), also set the database type as you wish in the bash script
1-postgres
2-mysql
3-mongo
I have specified the value of variables that needs to be passed during runtime to the python script in the bash script itself, so after adding these values you can run this bash script in your crontab after adding the value in .env.
Note: If you want to set this for postgres, set this under the postgres' user crontab

Now for the .env file, create a .env file in the same location where the python script resides and copy the .env_file from the repository and add the values as per your requirement, I have specified the values that need to added to each environment variables.
After all of this is set, run the bash script switch.sh in the crontab and you should be good.


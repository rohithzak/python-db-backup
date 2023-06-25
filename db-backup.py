import os
import sys
import smtplib
from dotenv import load_dotenv

load_dotenv()

# Functions to take database backups
def create_pg_dump(db_name, dump_file):
    dump_command = f'pg_dump -U postgres -d {db_name} > {dump_file}'
    return os.system(dump_command)

def create_mysqldump(username, password, db_name, dump_file):
    dump_command = f'mysqldump -u {username} -p{password} {db_name} --no-tablespaces  > {dump_file}'
    return os.system(dump_command)

def create_mongodump(db_name, username, password, dump_file):
    dump_command = f'mongodump -h localhost -d {db_name} -u {username} -p {password} -o {dump_file}'
    return os.system(dump_command)

# Function to push file to S3
def s3_push(source, profile,  s3_URL):
    push_command = f'aws --profile {profile} s3 cp {source} {s3_URL}'
    return os.system(push_command)

def cp_file(source, destination):
    cp_command = f'cp -r {source} {destination}'
    return os.system(cp_command)

# Function to copy file to another server
def scp_file(pem_file, source, user, ip, dest):
    scp_command = f'scp -i {pem_file} {source} {user}@{ip}:{dest}'
    return os.system(scp_command)

def send_email(state, body):
    sender = os.getenv('SENDER_EMAIL')
    receivers = os.getenv('RECEIVER_EMAILS').split(',')

    subject = f"Backup status: {state}"
    message = f"From: {sender}\nTo: {', '.join(receivers)}\nSubject: {subject}\n\n{body}"

    try:
        smtp = smtplib.SMTP('smtp.gmail.com', port='587')
        smtp.ehlo()
        smtp.starttls()
        smtp.login('humblesupport1@gmail.com', os.getenv('SENDER_PASSWORD'))
        smtp.sendmail(sender, receivers, message)
        smtp.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

cron = 0

if cron == 0:
    # Take database backup
    database_type = input("Enter database type (pg, mysql, mongo): ")

    if database_type == 'pg':
        database_name = input("Enter PostgreSQL database name: ")
        dump_file_name = input("Enter dump file name: ")
        status = create_pg_dump(database_name, dump_file_name)
    elif database_type == 'mysql':
        username = input("Enter username: ")
        password = input("Enter your password: ")
        database_name = input("Enter MySQL database name: ")
        dump_file_name = input("Enter dump file name: ")
        status = create_mysqldump(username, password, database_name,  dump_file_name)
    elif database_type == 'mongo':
        database_name = input("Enter MongoDB database name: ")
        username = input("Enter username: ")
        password = input("Enter your password: ")
        dump_file_name = input("Enter dump file name: ")
        status = create_mongodump(database_name, username, password, dump_file_name)
    else:
        print("Invalid database type.")
        exit(1)


    # Perform desired action (S3 or SCP) after database backup
    action = input("Do you want to use (s3, scp or cp) after taking the database backup? (yes/no): ")

    if action.lower() == 'yes':
        action_type = input("Enter the action type (s3, scp cp): ")

        if action_type == 's3':
            cp_source_path = input("Enter your cp_source path: ")
            url = input("Enter your S3 URL: ")
            profile = input("Enter your profile name")
            status = s3_push(cp_source_path, profile,  url)

        elif action_type == 'cp':
            cp_source_path = input("Enter your cp_source path: ")
            dest = input("Enter your destination path: ")
            status = cp_file(cp_source_path, dest)

        elif action_type == 'scp':
            pem = input("Enter your pem file path: ")
            cp_source = input("Enter your cp_source file path: ")
            user = input("Enter your remote user username: ")
            ip = input("Enter your remote IP Address: ")
            dest = input("Enter your remote destination: ")
            status = scp_file(pem, cp_source, user, ip, dest)
        else:
            print("Invalid action type.")


else:
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    database_type = 0
    action = 'null'

    if database_type == 1:
        status = create_pg_dump(arg1, arg2)
        if status == 0:
            send_email("Success", "PostgreSQL backup created successfully.")
        else:
            send_email("Failure", "Failed to create PostgreSQL backup.")
    elif database_type == 2:
        arg3 = sys.argv[3]
        arg4 = sys.argv[4]
        status = create_mysqldump(arg1, arg2, arg3, arg4)
        if status == 0:
            send_email("Success", "MySQL backup created successfully.")
        else:
            send_email("Failure", "Failed to create MySQL backup.")
    elif database_type == 3:
        arg3 = sys.argv[3]
        arg4 = sys.argv[4]
        status = create_mongodump(arg1, arg2, arg3, arg4)
        if status == 0:
            send_email("Success", "MongoDB backup created successfully.")
        else:
            send_email("Failure", "Failed to create MongoDB backup.")
    
    if action.lower() == 's3':
        source = os.getenv('S3_SOURCE')
        url = os.getenv('S3_URL')
        profile = os.getenv('S3_PROFILE')
        status = s3_push(source, profile,  url)
        if status == 0:
            send_email("Success", "File pushed to S3 successfully.")
        else:
            send_email("Failure", "Failed to push file to S3.")
    elif action.lower() == 'scp':
        pem = os.getenv('SCP_PEM')
        source = os.getenv('SCP_SOURCE')
        user = os.getenv('SCP_USER')
        ip = os.getenv('SCP_IP')
        dest = os.getenv('SCP_DEST')
        status = scp_file(pem, source, user, ip, dest)
        if status == 0:
            send_email("Success", "File transferred via SCP successfully.")
        else:
            send_email("Failure", "Failed to transfer file via SCP.")
    elif action.lower() == 'cp':
        source = os.getenv('CP_SOURCE')
        dest = os.getenv('CP_DEST')
        status = cp_file(source, dest)

        if status == 0:
            send_email("Success", "File transferred via CP successfully.")
        else:
            send_email("Failure", "Failed to transfer file via CP.")
    elif action.lower() == 'no':
        print("No action taken after the database backup.")
    else:
        print("Invalid action type.")

from db.mongo import uri
import subprocess
import os
import datetime


def backup(backup_path = "./"):

    # Execute the mongodump command
    subprocess.run(["mongodump", "--uri", f"\"{uri}\"", "--out", backup_path])
    # subprocess.run(["mongodump", "--uri", f"\"{uri}\""])

def restore(backup_path = "./"):
    # Execute the mongorestore command
    subprocess.run(["mongorestore", "--uri", f"\"{uri}\"", "--drop", backup_path])

if __name__ == "__main__":
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    backup(os.path.join("./backup/", timestamp))
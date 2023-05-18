from db.mongo import uri
import subprocess
import os
import sys


backup_folder_path = './backup/'

def get_latest_backup(path):
    subfolders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    latest_folder = max(subfolders, key=lambda x: os.path.getmtime(os.path.join(path, x)))
    return latest_folder

def restore(backup_path = os.path.join(backup_folder_path, get_latest_backup(backup_folder_path))):
    subprocess.run(["mongorestore", "--uri", f"\"{uri}\"", "--drop", backup_path])

def list_backup(path):
    subfolders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    for i,backup in enumerate(subfolders):
        print(backup)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "ls":
            list_backup(backup_folder_path)
        else:
            backup_ver = sys.argv[1]
            if os.path.isdir(os.path.join(backup_folder_path, backup_ver)):
                restore(os.path.join(backup_folder_path, backup_ver))
            else:
                print("not found")
    else: 
        restore()       


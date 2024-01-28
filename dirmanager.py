import sys
import os
import json
import shutil
import logging
from datetime import datetime

CONFIG_FILE_PATH = None
# sets config file from arg
if len(sys.argv) >= 2:
    CONFIG_FILE_PATH = sys.argv[1]

# loads config file when informed
if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, "r", encoding='utf-8') as config_file:
        user_config = json.load(config_file)
else:
    user_config = {}

# returns os default download dir
def get_default_download_dir():
    home_dir = os.path.expanduser("~")

    if os.name == 'posix':
        return os.path.join(home_dir, 'Downloads')
    elif os.name == 'nt':
        return os.path.join(os.path.join(home_dir, 'Downloads'))

# sets main config to config file : default
TARGET_DIR = user_config.get("targetDir", get_default_download_dir())
DEL_DIR = user_config.get("delDir", "delete")
TO_BE_DELETED = os.path.join(TARGET_DIR, DEL_DIR)
LOG_FILE = user_config.get("logFile", None)
EXP_DATE = user_config.get("expDate", 30)

# sets dir names to config file : default
TEXT = user_config.get("textDir", "text")
IMG = user_config.get("imgtDir", "image")
AUDIO = user_config.get("audioDir", "audio")
ZIP = user_config.get("zipDir", "zip")
VIDEO = user_config.get("videoDir", "video")
MISC = user_config.get("miscDir", "misc")

# file extension tuples
text_ext = (".txt", ".md", ".docx", ".pdf")
image_ext = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
audio_ext = (".mp3", ".wav", ".flac", ".aac", ".ogg")
zip_ext = (".zip", ".tar", ".gz", ".rar")
video_ext = (".mp4", ".mkv", ".avi", ".mov", ".wmv")

# returns appropriate file dir according to file extension
def get_file_folder(f_ext):
    if f_ext in text_ext:
        return os.path.join(TARGET_DIR, TEXT)
    elif f_ext in image_ext:
        return os.path.join(TARGET_DIR, IMG)
    elif f_ext in audio_ext:
        return os.path.join(TARGET_DIR, AUDIO)
    elif f_ext in zip_ext:
        return os.path.join(TARGET_DIR, ZIP)
    elif f_ext in video_ext:
        return os.path.join(TARGET_DIR, VIDEO)
    else:
        return os.path.join(TARGET_DIR, MISC)

# logs a message if LOG_FILE was informed
def log(msg):
    if LOG_FILE:
        logging.info(msg)

# moves file according to its extension
def move_file(file, source_path):
    f_name, f_ext = os.path.splitext(file)
    f_folder = get_file_folder(f_ext)
    if not os.path.exists(f_folder):
        os.mkdir(f_folder)

    dest_path = os.path.join(f_folder, file)
    log(f"Moving {source_path} to {dest_path}")
    shutil.move(source_path, dest_path)

# moves old files to TO_BE_DELETED
def move_to_old(file, source_path):
    if not os.path.exists(TO_BE_DELETED):
        os.mkdir(TO_BE_DELETED)
        
    dest_path = os.path.join(TO_BE_DELETED, file)
    log(f"Moving {source_path} to {dest_path}")
    shutil.move(source_path, dest_path)

# checks for empty directory
def is_dir_empty(dir_path):
    return not os.listdir(dir_path)

# determines whether it's a directory managed by dirmanager.py
def is_dir_managed(dir):
    return dir in {TEXT, IMG, AUDIO, ZIP, VIDEO, MISC}

def main():
    # sets log file when informed
    if LOG_FILE:
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO, encoding='utf-8')

    if not os.path.exists(TARGET_DIR):
        return

    # moves all files according to their extension
    for file in os.listdir(TARGET_DIR):
        file_path = os.path.join(TARGET_DIR, file)
        if not file.startswith('.') and os.path.isfile(file_path):
            move_file(file, file_path)

    # iterates all files in TARGET_DIR
    # moves all files older than EXP_DATE to TO_BE_DELETED
    # removes all empty directories
    for dir in os.listdir(TARGET_DIR):
        dir_path = os.path.join(TARGET_DIR, dir)
        if os.path.isdir(dir_path) and is_dir_managed(dir):
            if is_dir_empty(dir_path):
                log(f"Removed empty folder: {dir_path}")
                os.rmdir(dir_path)
                continue

            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                last_mod = datetime.fromtimestamp(os.path.getmtime(file_path))
                current_datetime = datetime.now()
                diff = current_datetime - last_mod
                if diff.days >= EXP_DATE:
                    move_to_old(file, file_path)

main()
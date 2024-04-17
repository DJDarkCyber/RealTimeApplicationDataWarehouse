import subprocess
import time

def get_clipboard_contents_linux():
    return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode()

clipboard_content = get_clipboard_contents_linux()
f = open("clipboard.txt", "a")
f.write(clipboard_content + "\n")
f.close()

while True:
    new_clipboard_content = get_clipboard_contents_linux()
    if clipboard_content != new_clipboard_content:
        clipboard_content = new_clipboard_content
        print(clipboard_content)
        f = open("clipboard.txt", "a")
        f.write(clipboard_content + "\n")
        f.close()
    
    time.sleep(1)
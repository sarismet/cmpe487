import threading
import os
import subprocess
import json
import sys
import re

port = 12345
def my_server():

    while(True):
        cmd = 'nc -l -p {}'.format(port)
        process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        encoding='utf-8',
        errors='replace'
        )
        out = process.stdout.readline()
        print(out)

    

def client(message,to):
    try:
        command = 'echo {} | nc {} {} -c'.format(message,to,port)
        subprocess.call(command, shell=True)
    except:
        pass


def create_ip_list(local_ip,lan):
    all_ips = {} 
    for ipx in range(256): 
        ip = lan+"."+str(ipx)
        name = "user{}".format(str(ipx))
        if ip != local_ip:
            all_ips[ip] = name

    json_object = json.dumps(all_ips, indent = 4)

    with open("ips.json", "w") as outfile: 
        outfile.write(json_object) 

def get_local_ips():
    local_ip = subprocess.getoutput("ipconfig getifaddr en0")
    parse=local_ip.split(".")
    lan=str(parse[0])+"."+str(parse[1])+"."+str(parse[2])
    return (local_ip,lan)

def send_discovery(my_ip):


    data={"MY_IP":"",
        "NAME":"USER",
        "TYPE":"DISCOVER",
        "PAYLOAD":""}
    data["MY_IP"]=my_ip
    
    outfile = open("ips.json", "r") 
    json_dict = json.load(outfile)
    for key in json_dict:
        msg = "\'"+json.dumps(data)+"\'"
        try:
            
            cmd = 'echo {} | nc {} {}'.format(msg,key,port)
            subprocess.Popen(cmd, shell=True)
        except:
            pass

    sys.stdout.flush()
            


if __name__ == "__main__":
    t=get_local_ips()
    create_ip_list(local_ip=t[0],lan=t[1])
    send_discovery(t[0])
    server = threading.Thread(target=my_server)
    server.start()
  
    

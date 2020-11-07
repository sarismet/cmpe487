import threading
import os
import subprocess
import json
import sys

def my_server():




    process = subprocess.Popen(
    'nc -l -p 12345',
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True,
    encoding='utf-8',
    errors='replace'
    )
    index=0
    while True:
        index=index + 1
        out = process.stdout.readline()
        if out == '' and process.poll() != None:
            break
        if out != '':
            
            sys.stdout.write(out)
            sys.stdout.flush()
            if out =="}":
                break
        
    

def client(message,to):
    command = 'echo {} | nc {} 12345 -c'.format(message,to)
    subprocess.call(command, shell=True)


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

if __name__ == "__main__":
    t=get_local_ips()
    create_ip_list(local_ip=t[0],lan=t[1])
    server = threading.Thread(target=my_server)
    server.start()
    data={"MY_IP":"192.168.1.3",
          "NAME":"USER",
          "TYPE":"DISCOVER",
          "PAYLOAD":""}
    msg=json.dumps(data)
    client = threading.Thread(target=client,args=(msg,str(t[0])))
    client.start()
    
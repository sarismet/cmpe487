import threading
import os
import subprocess
import json
import sys
import re
import time
import netifaces
port = 12345


def my_server(local_ip,response_json):

    while(True):
        try:
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
            print("out is ",out,flush=True)
            start=out.find('{')
            end=out.find('}')+1
            msg=out[start:end]
            files = open("l.txt","w")
            files.write(out)
            files.close()
            rejson = json.loads(msg)
            if rejson["TYPE"] == "DISCOVER":
                response_msg = {
                    "MY_IP":"",
                    "NAME":"",
                    "TYPE":"RESPOND",
                    "PAYLOAD":""
                }
                lan_turn=local_ip.split(".")[3]
                username= "USER"+str(lan_turn)
                response_msg["MY_IP"]=local_ip
                response_msg["NAME"] = username
                
                client(json.dumps(response_msg),rejson["MY_IP"])
            elif rejson["TYPE"] == "RESPOND":
                print()
                response_json[rejson["MY_IP"]]=rejson["NAME"]
                with open("response_json.json", "w") as outfile: 
                    outfile.write(json.dumps(response_json))
            else:
                os.system("clear")
                print("msg is ",msg,flush=True)
                
            sys.stdout.flush()
        except Exception as e:
            print("There is an error \n",e,flush=True)
    

def client(message,to):
    try:
        command = "echo '{}' | nc {} {} -c".format(message,to,port)
        print("sending the message with the command ",command,flush=True)
        subprocess.call(command, shell=True)
    except:
        pass




def get_local_ips(is_hamachi):
    local_ip = ""
    if is_hamachi:
        for i in netifaces.interfaces():
            for l in netifaces.ifaddresses(i).get(netifaces.AF_INET, ()):
                if l['addr'].startswith('25.'):
                    local_ip = l['addr']
    else:
        local_ip = subprocess.getoutput("ipconfig getifaddr en0")
    parse=local_ip.split(".")
    lan=str(parse[0])+"."+str(parse[1])+"."+str(parse[2])
    return (local_ip,lan)

def send_discovery(local_ip,lan):
    data={"MY_IP":"",
        "NAME":"ismet",
        "TYPE":"DISCOVER",
        "PAYLOAD":""}
    data["MY_IP"]=local_ip
    for last_number in range(0,256):
        temp_ip = lan+"."+str(last_number)
        if temp_ip != local_ip:
            print("sending discovery to ",temp_ip)
        msg = "\'"+json.dumps(data)+"\'"
        try:
            cmd = "echo '{}' | nc {} {}".format(msg,temp_ip,port)
            subprocess.Popen(cmd, shell=True)
        except:
            pass

    sys.stdout.flush()
            
def input_process(my_ip):
    os.system("clear")
    while(True):
        request = input("Whay do yo want to do \n Press m to send message\n Press d to send spesific discovery to an ip address")
        if request == "m":
            print('Write you messsage',flush=True)
            your_message=input()
            os.system("clear")
            json_data={"MY_IP":"",
                        "NAME":"USER",
                        "TYPE":"MESSAGE",
                        "PAYLOAD":""}
            json_data["MY_IP"] = my_ip
            json_data["PAYLOAD"] = your_message
            msg=json.dumps(json_data)
            print('Which ip do you want to send this message',flush=True)
            ip_to_send=input()

            """discovery_data={"MY_IP":"",
                        "NAME":"USER",
                        "TYPE":"DISCOVER",
                        "PAYLOAD":""}
            discovery_data["MY_IP"]=my_ip

            client(json.dumps(discovery_data),ip_to_send)"""
            print("msg is ",msg,flush=True)
            client(msg,ip_to_send)
        elif request == "d":
            print('Write the ip address',flush=True)
            ip_to_send=input()
            os.system("clear")
            json_data={"MY_IP":"",
                        "NAME":"ismet",
                        "TYPE":"DISCOVER",
                        "PAYLOAD":""}
            json_data["MY_IP"] = my_ip
            msg=json.dumps(json_data)
            print("msg is ",msg,flush=True)
            client(msg,ip_to_send)
        else:
            input_process(my_ip)

if __name__ == "__main__":
    response_json={}
    with open("response_json.json", "r") as outfile: 
        response_json = json.load(outfile)
    
    hamachi = False
    try:
        if sys.argv[1] == "h":
            hamachi = True
    except:
        pass
    t=get_local_ips(hamachi)
    """discovery_thread = threading.Thread(target=send_discovery,args=(t[0],t[1],))
    discovery_thread.start()
    discovery_thread.join()"""
    server = threading.Thread(target=my_server,args=(t[0],response_json,))
    server.start()

    input_process(my_ip=t[0])
    
  
    

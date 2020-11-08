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
            start=out.find('{')
            end=out.find('}')+1
            msg=out[start:end]
            rejson = json.loads(msg)
            print("the json loaded is :",rejson,flush=True)
            if rejson["TYPE"] == "DISCOVER":
                response_msg = {
                    "MY_IP":"",
                    "NAME":"",
                    "TYPE":"RESPOND",
                    "PAYLOAD":""
                }
                is_writable = True
                responses = response_json["response_array"]
                for response in responses:
                    if response["ip"] == rejson["MY_IP"]:
                        is_writable = False
                if is_writable:
                    response_json["response_array"].append({"user_name":rejson["NAME"],"ip":rejson["MY_IP"]})
                    with open("response_json.json", "w") as outfile: 
                        outfile.write(json.dumps(response_json))

                response_msg["MY_IP"]=local_ip
                response_msg["NAME"] = "ismet"
                client(json.dumps(response_msg),rejson["MY_IP"])
                log_file = open("log.txt","a")
                log_file.write("you got a DISCOVER message from "+rejson["MY_IP"]+" so send a RESPOND message \n")
                log_file.close()
            elif rejson["TYPE"] == "RESPOND":
                
                is_writable = True
                responses = response_json["response_array"]
                for response in responses:
                    if response["ip"] == rejson["MY_IP"]:
                        is_writable = False
                if is_writable:
                    response_json["response_array"].append({"user_name":rejson["NAME"],"ip":rejson["MY_IP"]})
                    with open("response_json.json", "w") as outfile: 
                        outfile.write(json.dumps(response_json))

                log_file = open("log.txt","a")
                log_file.write("you got a RESPOND message from "+rejson["MY_IP"]+"\n")
                log_file.close()
            else:
                log_file = open("log.txt","a")
                log_file.write("you got a MESSAGE message from "+rejson["MY_IP"]+" which is "+rejson["PAYLOAD"]+"\n")
                log_file.close()
                os.system("clear")
                print("msg is ",msg,flush=True)
                
            print("Whay do yo want to do \n Press m to send message\n Press d to send spesific discovery to an ip address\n",flush=True)
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
            log_file = open("log.txt","a")
            log_file.write("you send a DISCOVER message to "+temp_ip+"\n")
            log_file.close()
            msg = json.dumps(data)
            try:
                cmd = "echo '{}' | nc {} {}".format(msg,temp_ip,port)
                subprocess.Popen(cmd, shell=True)
            except:
                pass

    sys.stdout.flush()
            
def input_process(my_ip):
    os.system("clear")
    while(True):
        request = input("Whay do yo want to do \n Press m to send message\n Press d to send spesific discovery to an ip address\n")
        if request == "m":
            print('Write you messsage\n',flush=True)
            your_message=input()
            os.system("clear")
            json_data={"MY_IP":"",
                        "NAME":"ismet",
                        "TYPE":"MESSAGE",
                        "PAYLOAD":""}
            json_data["MY_IP"] = my_ip
            json_data["PAYLOAD"] = your_message
            msg=json.dumps(json_data)
            print('Which user do you want to send this message\n',flush=True)
            responses = response_json["response_array"]
            index = 1
            for response in responses:
                print(index,".",response["user_name"],"\n",flush=True)
                index = index + 1
            user_order=int(input("give order\n"))
            
            ip_to_send = response_json["response_array"][user_order-1]["ip"]
            client(msg,ip_to_send)
            log_file = open("log.txt","a")
            log_file.write("you send a MESSAGE message to "+ip_to_send+"\n")
            log_file.close()
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
            client(msg,ip_to_send)
            log_file = open("log.txt","a")
            log_file.write("you send a DISCOVER message to "+ip_to_send+"\n")
            log_file.close()
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
    server = threading.Thread(target=my_server,args=(t[0],response_json,))
    server.start()
    time.sleep(2)
    discovery_thread = threading.Thread(target=send_discovery,args=(t[0],t[1],))
    discovery_thread.start()
    discovery_thread.join()
    

    input_process(my_ip=t[0])

    
  
    

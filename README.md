# Storage Manager


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)


# Files Structures

  - There is only one directory and you can find all the files.
  - There is a file named as requirements.txt and you can find all the dependencies.

# Important:
  - I have tried this app with my friend Alkım Ece Toprak, Özgürcan Öztaş and Muhammed Tayyip Yazıcı.
  - There is a log file named as log.txt and it is in charge of keeping all the logs of history of communication.
  - The other file response_json.json that includes a response_array which is an array that keeps the username and ips of users
  
  ![alt text](https://github.com/sarismet/cmpe487/blob/main/responsearray.png)
  
  - The app first start server and beings listening then send the DISCOVER message to ips in its lan such that if our ip is 25.43.1.132 then it sends 25.43.1.0. to 25.43.1.255.
  - After that the app ask you what you want to do. You can send message if you know the ip before or you need to send a spesific DISCOVER message to get response and know the ip to send a message.
  ![alt text](https://github.com/sarismet/cmpe487/blob/main/what.png)
  
  - To send a message press m then app list the known users and ask you to give the order of the user that you want to send the message
  
  ![alt text](https://github.com/sarismet/cmpe487/blob/main/message1.png)
  
  ![alt text](https://github.com/sarismet/cmpe487/blob/main/message2.png)
  
  - To send a DISCOVER message press d then enter the ip
  ![alt text](https://github.com/sarismet/cmpe487/blob/main/discover.png)
  


### Run the program:
- To run on LogMeIn Hamachi
```sh
$ python3 app.py h
```
- - To run on Localhost
```sh
$ python3 app.py l
```


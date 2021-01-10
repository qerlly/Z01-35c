from tkinter import *
import sqlite3
from flask import request, jsonify
from urllib.request import urlopen
import os
import io
import requests
import json
from tkinter.ttk import Combobox
import datetime
from dateutil import parser
import operator
import socketio

sio = socketio.Client()
usrnm = ""

class UserApp:
  def __init__(self, login, combo, area):
    self.login = login
    self.combo = combo
    self.area = area

  def get_t(self):
    return self.area
        
  def set_t(self, area):
    self.area = area

  def get_c(self):
    return self.combo
        
  def set_c(self, combo):
    self.combo = combo
  
  def get_u(self):
    return self.login
        
  def set_u(self, login):
    self.login = login 
   
  def readMes(self, userFrom):
    nmz = userFrom.split(",")[0]
    if userFrom == "all":
        urlm = "http://127.0.0.1:5000/api/v1/resources/messages/to?userTo=all"
    else :
        urlm = "http://127.0.0.1:5000/api/v1/resources/messages/users?userFrom="+str(nmz)+"&userTo="+str(self.login)
        urlc = "http://127.0.0.1:5000/api/v1/resources/messages/users?userFrom="+str(self.login)+"&userTo="+str(nmz)
    responsem = requests.get(urlm)
    msgs_data = json.loads(responsem.text)
    if nmz != "all":
        responsemc = requests.get(urlc)
        msgs_datac = json.loads(responsemc.text)
        mess_data = msgs_data + msgs_datac
    else :
        mess_data = msgs_data
        
    i = 0
      
    for msgz in mess_data:
        if(msgz["fromUser"] != self.login):
            res = requests.post('http://127.0.0.1:5000/api/v1/resources/messages/read/' + msgz["datatime"], json={"login":msgz["fromUser"],"datatime":msgz["datatime"],"status":"read"})    
            sio.emit('read_message')
    checkOnline(self.combo, usrnm)
    valr = self.combo.get()
    if nmz != "all":
        masz = valr.split(",")
        masz[1] = "0"
        valr = masz[0] + ", " + masz[1] + "," + masz[2]
        self.combo.set(valr)
    self.getMes(self.combo.get(), userApp.get_t())    
    
  def getMes(self, userFrom, textArea):
    nmz = userFrom.split(",")[0]
    if userFrom == "all":
        urlm = "http://127.0.0.1:5000/api/v1/resources/messages/to?userTo=all"
    else :
        urlm = "http://127.0.0.1:5000/api/v1/resources/messages/users?userFrom="+str(nmz)+"&userTo="+str(self.login)
        urlc = "http://127.0.0.1:5000/api/v1/resources/messages/users?userFrom="+str(self.login)+"&userTo="+str(nmz)
    responsem = requests.get(urlm)
    msgs_data = json.loads(responsem.text)
    if nmz != "all":
        responsemc = requests.get(urlc)
        msgs_datac = json.loads(responsemc.text)
        mess_data = msgs_data + msgs_datac
    else :
        mess_data = msgs_data
        
    textArea.delete('1.0', END)     
    i = 0
     
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(mess_data) - 1):
            if parser.parse(mess_data[i]["datatime"]) > parser.parse(mess_data[i + 1]["datatime"]):
                mess_data[i], mess_data[i + 1] = mess_data[i + 1], mess_data[i]
                swapped = True
      
    for msgz in mess_data:
        if(msgz["fromUser"] != self.login):
            textArea.insert(INSERT, "From: " + str(msgz["fromUser"]) + " " + msgz["datatime"] +"\n")
            if msgz["status"] == "unread":
                textArea.insert(INSERT, "  message: " + str(msgz["msg"]) + "\n", 'RED')
                textArea.tag_config('RED', foreground='red')
            else:
                textArea.insert(INSERT, "  message: " + str(msgz["msg"]) + "\n")
                textArea.tag_config('RED', foreground='red')
        else:
            textArea.insert(INSERT, "\t\t\t\t\t\t\t\tFrom: " + str(self.login) + " " + msgz["datatime"] + "\n")
            textArea.insert(INSERT, "\t\t\t\t\t\t\t\t  message: " + str(msgz["msg"]) + "\n", 'BLUE')
            textArea.tag_config('BLUE', foreground='blue')

    
  def sendMes(self, userTo, textArea, msg):
    textArea.insert(INSERT, "\t\t\t\t\tFrom: " + str(self.login) + "\n")
    textArea.insert(INSERT, "\t\t\t\t " + msg.get() + "\n", 'BLUE')
    textArea.tag_config('BLUE', foreground='blue')

    name = userTo.split(",")[0]
    res = requests.post("http://127.0.0.1:5000/api/v1/resources/messages/" + self.login + "/add/"+str(name), json={"userFrom":self.login,"userTo":name, "message":msg.get(), "datetime":str(datetime.datetime.now()), "status":"unread"})   
    msg.set("")
    return


logWindow = Tk()  
logWindow.geometry('300x150')  
logWindow.title('Login Form')
userApp = UserApp("", None, None)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def checkForLogin(username):
    url = "http://127.0.0.1:5000/api/v1/resources/users/all"
    response = requests.get(url)
    data = json.loads(response.text)
    for entry in data:
        print(entry["login"])
        if username == entry["login"]:
            return True
    return False


def checkOnline(cb, login):
    urlo = "http://127.0.0.1:5000/api/v1/resources/users/all"
    responseo = requests.get(urlo)
    userso_data = json.loads(responseo.text)
    online_list = []
    for entry in userso_data:
        mas = []
        mas.append(entry["login"])
        
        urlm = "http://127.0.0.1:5000/api/v1/resources/messages/users?userFrom="+str(entry["login"])+"&userTo="+str(userApp.get_u())
        responsem = requests.get(urlm)
        usersm_data = json.loads(responsem.text)
        
        counter = 0
        date = ""
        for msg in usersm_data:
            if msg["status"] == "unread":
                counter+=1
            date = msg["datatime"]
        
        mas.append(str(counter))
        mas.append(date)
        mas.append(entry["status"])
        online_list.append(mas)
        
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(online_list) - 1):
            if online_list[i][3] < online_list[i + 1][3]:
                online_list[i], online_list[i + 1] = online_list[i + 1], online_list[i]
                swapped = True 

    swapped = True
    while swapped:
        swapped = False
        for i in range(len(online_list) - 1):
            if online_list[i][2] < online_list[i + 1][2]:
                online_list[i], online_list[i + 1] = online_list[i + 1], online_list[i]
                swapped = True                
    
    str_mas=[]
    for ms in online_list:
        if str(ms[0]) != str(userApp.get_u()):
            str_mas.append(str(ms[0]) + ", " + str(ms[1]) + ", " + str(ms[3]))    
    str_mas.append("all")
    cb["values"] = str_mas


def userForm(user):
    url = "http://127.0.0.1:5000/api/v1/resources/users/all"
    response = requests.get(url)
    users_data = json.loads(response.text)
    
    userWindow = Toplevel(logWindow) 
    userWindow.title("Czat user - " + str(user)) 
    userWindow.geometry("900x400") 
    userWindow.protocol('WM_DELETE_WINDOW',donothing)
    logWindow.withdraw()
    users_list = ["all"]
    for entry in users_data:
        if entry["login"] != user:
            users_list.append(entry["login"])
            
    textArea = Text(userWindow, height = 15, width = 105)
    textArea.grid(row=1, columnspan=2) 
    usernameLabel = Label(userWindow, text="Message for:").grid(row=0, column=0)
    
    comboUser = Combobox(userWindow, font=("Arial Bold", 16), state='readonly')
    userApp.set_u(str(user))
    userApp.set_c(comboUser)
    userApp.set_t(textArea)
    comboUser["values"] = users_list
    comboUser.current(0)
    comboUser.grid(row=0, column=1, padx=(10, 10)) 
    comboUser.bind("<<ComboboxSelected>>", lambda event: userApp.getMes(comboUser.get(), textArea))
    checkOnline(comboUser, user)
    userApp.getMes(comboUser.get(), textArea)    
        
    msgLabel = Label(userWindow,text="Write your message:", font=("Arial Bold", 16)).grid(row=3, column=0)  
    msg = StringVar()
    msgEntry = Entry(userWindow, textvariable=msg, font=("Arial Bold", 16)).grid(row=3, column=1)  

    readButton = Button(userWindow, text="Read", command=lambda: userApp.readMes(comboUser.get())).grid(row=4, column=0)  
    sendButton = Button(userWindow, text="Send", command=lambda: userApp.sendMes(comboUser.get(), textArea, msg)).grid(row=4, column=1)  
    backButton = Button(userWindow, text="Logout", command=lambda: logout(userWindow, userApp.login)).grid(row=4, column=2)


def validateLogin(username, password):
    url = "http://127.0.0.1:5000/api/v1/resources/users/all"
    response = requests.get(url)
    data = json.loads(response.text)
    for entry in data:
        if username == entry["login"] and password == entry["password"]:
            print("Logowanie udało się")
            res = requests.post('http://127.0.0.1:5000/api/v1/resources/users/online/add/' + str(username), json={"login":username,"czas":str(datetime.datetime.now())})   
            resz = requests.post('http://127.0.0.1:5000/api/v1/resources/users/login/' + str(username), json={"login":username,"status":"online"}) 
            userForm(entry["login"])
            sio.connect('http://127.0.0.1:5000')
            usrnm = str(username)
            return
    print("Błędne parametry")
    
    
@sio.event
def message():
    print("mess")
    checkOnline(userApp.get_c(), usrnm)
    userApp.getMes(userApp.get_c().get(), userApp.get_t())    
    checkOnline(userApp.get_c(), usrnm)

@sio.event
def login():
    checkOnline(userApp.get_c(), usrnm)


def register(login, passw, repass, win):
    if checkForLogin(login):
        print("Użytkownik z takim loginem już istnieje")
        return
    if passw == repass:
        res = requests.post('http://127.0.0.1:5000/api/v1/resources/users/add/' + str(login), json={"login":login,"password":passw,"status":"offline"})   
        back(win)
    else:
        print("Hasła się nie zgadzają")    
    

def logout(win, user):
    win.destroy()
    sio.disconnect()
    usrnm = ""
    res = requests.delete('http://127.0.0.1:5000/api/v1/resources/users/online/delete/' + str(userApp.get_u()), json={"login":userApp.get_u(),"czas":str(datetime.datetime.now())})   
    res = requests.post('http://127.0.0.1:5000/api/v1/resources/users/login/' + str(userApp.get_u()), json={"login":userApp.get_u(),"status":"offline"})    
    logWindow.deiconify()
    
def back(win):
    win.destroy()
    userApp = None
    logWindow.deiconify()


def registerForm():
    regWindow = Toplevel(logWindow) 
    regWindow.title("Registration Form") 
    regWindow.geometry("300x150") 
    regWindow.protocol('WM_DELETE_WINDOW',donothing)
    logWindow.withdraw()
            
    loginLabel = Label(regWindow, text="Login").grid(row=0, column=0)
    log = StringVar()
    loginEntry = Entry(regWindow, textvariable=log).grid(row=0, column=1)  
    passLabel = Label(regWindow,text="Password").grid(row=1, column=0)  
    passw = StringVar()
    passEntry = Entry(regWindow, textvariable=passw, show='*').grid(row=1, column=1) 
    rpassLabel = Label(regWindow,text="Repeat password").grid(row=2, column=0)  
    rpassw = StringVar()
    rpassEntry = Entry(regWindow, textvariable=rpassw, show='*').grid(row=2, column=1) 
    
    newRegButton = Button(regWindow, text="Submit", command=lambda: register(log.get(), passw.get(), rpassw.get(), regWindow)).grid(row=4, column=0)  
    backButton = Button(regWindow, text="Back", command=lambda: back(regWindow)).grid(row=4, column=1) 


def donothing():
    pass


usernameLabel = Label(logWindow, text="Login").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(logWindow, textvariable=username).grid(row=0, column=1)  

passwordLabel = Label(logWindow,text="Password").grid(row=1, column=0)  
password = StringVar()
passwordEntry = Entry(logWindow, textvariable=password, show='*').grid(row=1, column=1)  

loginButton = Button(logWindow, text="Login", command=lambda: validateLogin(username.get(), password.get())).grid(row=4, column=0)  
regButton = Button(logWindow, text="Registration", command=registerForm).grid(row=4, column=1)  

logWindow.mainloop()
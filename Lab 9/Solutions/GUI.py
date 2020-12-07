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

class UserApp:
  def __init__(self, login):
    self.login = login
    
  def getMes(self, userFrom, textArea):
    if userFrom == "all":
        urlm = "http://127.0.0.1:5000/api/v1/resources/messages/to?userTo=all"
    else :
        urlm = "http://127.0.0.1:5000/api/v1/resources/messages/users?userFrom="+str(userFrom)+"&userTo="+str(self.login)
        urlc = "http://127.0.0.1:5000/api/v1/resources/messages/users?userFrom="+str(self.login)+"&userTo="+str(userFrom)
    responsem = requests.get(urlm)
    msgs_data = json.loads(responsem.text)
    if userFrom != "all":
        responsemc = requests.get(urlc)
        msgs_datac = json.loads(responsemc.text)
    textArea.delete('1.0', END)     
    i = 0
    for msgz in msgs_data:
        textArea.insert(INSERT, "From: " + str(msgz["fromUser"]) + "\n")
        textArea.insert(INSERT, "\t" + str(msgz["msg"]) + "\n")
        if userFrom != "all":
            if len(msgs_datac) > i :
                textArea.insert(INSERT, "\t\t\t\t\tFrom: " + str(self.login) + "\n")
                textArea.insert(INSERT, "\t\t\t\t " + str(msgs_datac[i]["msg"]) + "\n")
                i += 1
    
  def sendMes(self, userTo, textArea, msg):
    textArea.insert(INSERT, "\t\t\t\t\tFrom: " + str(self.login) + "\n")
    textArea.insert(INSERT, "\t\t\t\t " + msg.get() + "\n")

    res = requests.post("http://127.0.0.1:5000/api/v1/resources/messages/" + self.login + "/add/"+str(userTo), json={"userFrom":self.login,"userTo":userTo, "message":msg.get()})   
    msg.set("")
    return


logWindow = Tk()  
logWindow.geometry('300x150')  
logWindow.title('Login Form')
userApp = None


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


def checkOnline(cb):
    urlo = "http://127.0.0.1:5000/api/v1/resources/users/online/all"
    responseo = requests.get(urlo)
    userso_data = json.loads(responseo.text)
    online_list = []
    for entry in userso_data:
        online_list.append(entry["login"])
    cb["values"] = online_list


def userForm(user):
    userApp = UserApp(user)
    url = "http://127.0.0.1:5000/api/v1/resources/users/all"
    response = requests.get(url)
    users_data = json.loads(response.text)
    
    userWindow = Toplevel(logWindow) 
    userWindow.title("Czat user - " + str(user)) 
    userWindow.geometry("750x400") 
    userWindow.protocol('WM_DELETE_WINDOW',donothing)
    logWindow.withdraw()
    users_list = ["all"]
    for entry in users_data:
        if entry["login"] != user:
            users_list.append(entry["login"])
            
    textArea = Text(userWindow, height = 15, width = 55)
    textArea.grid(row=1, columnspan=2) 
    usernameLabel = Label(userWindow, text="Message for:").grid(row=0, column=0)
    
    comboOnline = Combobox(userWindow, font=("Arial Bold", 16), state='readonly')
    comboOnline.grid(row=0, column=2, padx=(10, 10))
    comboOnline.bind("<<ComboboxSelected>>", lambda event: checkOnline(comboOnline))
    checkOnline(comboOnline)
    
    comboUser = Combobox(userWindow, font=("Arial Bold", 16), state='readonly')
    comboUser["values"] = users_list
    comboUser.current(0)
    comboUser.grid(row=0, column=1, padx=(10, 10)) 
    comboUser.bind("<<ComboboxSelected>>", lambda event: userApp.getMes(comboUser.get(), textArea))
    userApp.getMes(comboUser.get(), textArea)    
        
    msgLabel = Label(userWindow,text="Write your message:", font=("Arial Bold", 16)).grid(row=3, column=0)  
    msg = StringVar()
    msgEntry = Entry(userWindow, textvariable=msg, font=("Arial Bold", 16)).grid(row=3, column=1)  

    sendButton = Button(userWindow, text="Send", command=lambda: userApp.sendMes(comboUser.get(), textArea, msg)).grid(row=4, column=0)  
    backButton = Button(userWindow, text="Logout", command=lambda: logout(userWindow, userApp.login)).grid(row=4, column=1)


def validateLogin(username, password):
    url = "http://127.0.0.1:5000/api/v1/resources/users/all"
    response = requests.get(url)
    data = json.loads(response.text)
    for entry in data:
        if username == entry["login"] and password == entry["password"]:
            print("Logowanie udało się")
            res = requests.post('http://127.0.0.1:5000/api/v1/resources/users/online/add/' + str(username), json={"login":username,"czas":str(datetime.datetime.now())})   
            userForm(entry["login"])
            return
    print("Błędne parametry")


def register(login, passw, repass, win):
    if checkForLogin(login):
        print("Użytkownik z takim loginem już istnieje")
        return
    if passw == repass:
        res = requests.post('http://127.0.0.1:5000/api/v1/resources/users/add/' + str(login), json={"login":login,"password":passw})   
        back(win)
    else:
        print("Hasła się nie zgadzają")    
    

def logout(win, user):
    win.destroy()
    userApp = None
    res = requests.delete('http://127.0.0.1:5000/api/v1/resources/users/online/delete/' + str(user), json={"login":user,"czas":str(datetime.datetime.now())})    
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
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter.ttk import Combobox
import os
import io
import requests
import json
from PIL import Image, ImageTk
import tkinter as tk
from urllib.request import urlopen
from datetime import datetime
import matplotlib.colors as mcolors

API_key = "0cc9c9637fddd86c23b53a46884c257d"
root = Tk()
root.title("Weather forecast")
root.geometry('700x350')
lat = "52.237049"
lon = "21.017532"
day = 0
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, API_key)
response = requests.get(url)
data = json.loads(response.text)


def changeCords(event):
    if comboС.get() == "Warsaw":
        lat = "52.237049"
        lon = "21.017532"
    elif comboС.get() == "London":
        lat = "51.509865"
        lon = "-0.118092"
    elif comboС.get() == "Moscow":
        lat = "55.644466"
        lon = "37.395744"
    elif comboС.get() == "Minsk":    
        lat = "53.893009"
        lon = "27.567444"
    elif comboС.get() == "Berlin":    
        lat = "52.520008"
        lon = "13.404954"
    if combo.get() == "Today":
        day = 0;
    elif combo.get() == "Tomorrow":
        day = 1;
    elif combo.get() == "After tomorrow":
        day = 2;
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, API_key)
    response = requests.get(url)
    data = json.loads(response.text)
    fcastD.configure(text=combo.get())
    fcastT.configure(text=data["daily"][day]["temp"]["day"])
    fcastTN.configure(text=data["daily"][day]["temp"]["night"])
    pic_url = "http://openweathermap.org/img/w/" + data["daily"][day]["weather"][0]["icon"] + ".png"
    my_page = urlopen(pic_url)
    my_picture = io.BytesIO(my_page.read())
    pil_img = Image.open(my_picture)
    tk_img = ImageTk.PhotoImage(pil_img)
    label.configure(image=tk_img)
    label.image = tk_img
    fcastW.configure(text=str(data["daily"][day]["clouds"]) + "%")
    hourlyObj = data["hourly"]
    arrTemp = []
    arrHour = []
    for entry in hourlyObj:
        arrTemp.append(entry["temp"])
        arrHour.append(datetime.fromtimestamp(entry["dt"]))
    
    fday = arrHour[0].day
    arrDays = [[], [], []]
    dayq = 0
    for dayz in arrHour:
        if dayz.day == fday:
            arrDays[dayq].append(dayz.hour)
        else: 
            fday = dayz.day 
            dayq +=1
            arrDays[dayq].append(dayz.hour)

    if day == 0:
        pltShow(arrTemp[:len(arrDays[0])], arrDays[day])
    elif day == 1:
        arrS = arrTemp[:(len(arrDays[0]) + len(arrDays[1]))]
        arrS = arrS[len(arrDays[0]):]
        pltShow(arrS, arrDays[day])
    else:
        pltShow(arrTemp[(len(arrDays[0]) + len(arrDays[1])):], arrDays[day])
   

def pltShow(tempz, timez):    
    h = plt.bar(timez, tempz, width=1)
    
    for i in range(len(timez)):
        h[i].set_facecolor(getColor(tempz[i]))
    
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.title("Temperature forecast")
    plt.show(block=False)
  
def getColor(tempC):
    if tempC < -5:
        return "navy"
    elif tempC < 1:
        return "blue"    
    elif tempC < 0:
        return "royalblue"
    elif tempC >= 0 and tempC <= 1:
        return "skyblue"
    elif tempC > 1 and tempC <= 2:
        return "lavender"
    elif tempC > 2 and tempC <= 3:
        return "lightyellow"
    elif tempC > 3 and tempC <= 4:
        return "lemonchiffon"
    elif tempC > 4 and tempC <= 5:
        return "y"
    elif tempC > 5 and tempC <= 6:
        return "yellow"
    elif tempC > 6 and tempC <= 7:
        return "gold"
    else:
        return "orange"
 
    
lbl = Label(root, text="Enter city", font=("Arial Bold", 18))  
lbl.grid(column=0, row=0)   
lbl2 = Label(root, text="Enter day", font=("Arial Bold", 18))  
lbl2.grid(column=2, row=0)
lbl3 = Label(root, text="Daily forecast", font=("Arial Bold", 18))  
lbl3.grid(column=0, row=3, pady=(30, 10))

comboС = Combobox(root, font=("Arial Bold", 20), state='readonly')  
comboС['values'] = ("Warsaw", "London", "Moscow", "Minsk", "Berlin")  
comboС.current(0)
comboС.grid(column=0, row=1, padx=(10, 10)) 
comboС.bind("<<ComboboxSelected>>", changeCords)

combo = Combobox(root, font=("Arial Bold", 20), state='readonly')  
combo['values'] = ("Today", "Tomorrow", "After tomorrow")  
combo.current(0)
combo.grid(column=2, row=1, padx=(10, 10))
combo.bind("<<ComboboxSelected>>", changeCords)

fcastD = Label(root, text=combo.get(), font=("Arial Bold", 18))  
fcastD.grid(column=0, row=4, padx=(10, 10))
fcastT = Label(root, text=data["daily"][day]["temp"]["day"], font=("Arial Bold", 18))  
fcastT.grid(column=0, row=5, padx=(10, 10))
fcastTN = Label(root, text=data["daily"][day]["temp"]["night"], font=("Arial Bold", 12))  
fcastTN.grid(column=0, row=6, padx=(10, 10))

pic_url = "http://openweathermap.org/img/w/" + data["daily"][day]["weather"][0]["icon"] + ".png"
my_page = urlopen(pic_url)
my_picture = io.BytesIO(my_page.read())
pil_img = Image.open(my_picture)
tk_img = ImageTk.PhotoImage(pil_img)
label = Label(root, image=tk_img)
label.image = tk_img
label.grid(column=0, row=7, sticky='ew')

fcastW = Label(root, text=str(data["daily"][day]["clouds"]) + "%", font=("Arial Bold", 18))  
fcastW.grid(column=0, row=8, padx=(10, 10))

hourlyObj = data["hourly"]
arrTemp = []
arrHour = []
for entry in hourlyObj:
    arrTemp.append(entry["temp"])
    arrHour.append(datetime.fromtimestamp(entry["dt"]))

fday = arrHour[0].day
arrDays = [[], [], []]
dayq = 0
for dayz in arrHour:
    if dayz.day == fday:
        arrDays[dayq].append(dayz.hour)
    else: 
        fday = dayz.day 
        dayq +=1
        arrDays[dayq].append(dayz.hour)
    
pltShow(arrTemp[:len(arrDays[0])], arrDays[0])

root.mainloop()
from flask import Flask
from flask import request
from flask import json
from flask import jsonify, make_response
from flask import Response, render_template, redirect
from datetime import datetime,date,time
import json
import math

from flask import Flask, render_template, redirect, request, url_for
import flask_login
from flask_login import LoginManager, UserMixin # for the login system

import requests


from flask_mysql_connector import MySQL

app = Flask(__name__)
app.secret_key = '7sqTmHwNwDDRt2savrym'


app.config['MYSQL_USER'] = 'Dorchester'
app.config['MYSQL_PASSWORD'] = 'hQR36hW8U24RA8Hw'
app.config['MYSQL_DATABASE'] = 'dorchester'
app.config['MYSQL_HOST'] = '127.0.0.1'
mysql = MySQL()

#dbPath = "/home/ubuntu/Sailing-Manager/DSC.db"
baseUrl = "https://development.dorchestersailingclub.org.uk/"

def entrylist():
    conn = mysql.connection
    mycursor = conn.cursor()

    mycursor.execute("SELECT * FROM Racers")
    data = mycursor.fetchall()
    return data

def startTimeList(racelen = 40):
    conn = mysql.connection
    mycursor = conn.cursor()

    mycursor.execute("SELECT DISTINCT Racers.Boat, PyList.PY FROM Racers INNER JOIN PyList ON Racers.Boat=PyList.Class ORDER BY PyList.py DESC")
    data = mycursor.fetchall()
    print(data)
    empty = True
    print(racelen)
    if len(data) > 0:
        correctedTime = (racelen/data[0][1])*1000
        #print(correctedTime)
        data[0] = list(data[0])
        data[0].append(0) # adds time from start colum
        
        #print(data)
        #print(correctedTime)

        for i in range(1,len(data)):
            
            elapsedTime = (correctedTime*data[i][1])/1000
            #print(elapsedTime)
            timeFromStart = racelen - round(elapsedTime)
            #print(timeFromStart)
            data[i] = list(data[i])
            data[i].append(timeFromStart)
        empty = False
        #print(empty)
        return data,empty
    else:
        empty = True
        #print(empty)
        return data,empty

def boats():
    boatList = []
    conn = mysql.connection
    mycursor = conn.cursor()

    mycursor.execute("SELECT Class,PY FROM PyList ORDER BY Class")
    
    rawboatList = mycursor.fetchall()
    #print(rawboatList)
    for items in rawboatList:
        boatList.append(items[0])   
    #print(boatList)
    
    return boatList

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def outOftimeSignUp():
    
    now = datetime.now()

    if now.weekday() == 6:
        conn = mysql.connection
        mycursor = conn.cursor()

        mycursor.execute("SELECT CutOffTime FROM oodSetup")

        timeNow = now.strftime("%H:%M:%S")
        
        cutofftime = mycursor.fetchone()
        cutofftime = str(cutofftime[0]) # date time
        cutofftimeseconds = int(get_sec(cutofftime))
        timeNowSeconds = get_sec(timeNow)
        print("cutoff",cutofftimeseconds)
        print("timenow",timeNowSeconds)
        if cutofftimeseconds > timeNowSeconds:
            #print(True)
            return True
        else:

            #print(False)
            return False
    else:
        return True
    
def getRaceType():
    conn = mysql.connection
    mycursor = conn.cursor()

    mycursor.execute("SELECT RaceType FROM oodSetup")
    
    data = mycursor.fetchone()

    return data

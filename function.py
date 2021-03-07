from flask import Flask
from flask import request
from flask import json
from flask import jsonify, make_response
from flask import Response, render_template, redirect
from datetime import datetime,date,time

import math

import requests


from flask_mysql_connector import MySQL


app.config['MYSQL_USER'] = 'Dorchester'
app.config['MYSQL_PASSWORD'] = 'hQR36hW8U24RA8Hw'
app.config['MYSQL_DATABASE'] = 'dorchester'
app.config['MYSQL_HOST'] = '127.0.0.1'
mysql = MySQL()

#import mysql.connector

#mydb = mysql.connector.connect(host="127.0.0.1",user="Dorchester",password="hQR36hW8U24RA8Hw",database="dorchester")



#dbPath = "/home/ubuntu/Sailing-Manager/DSC.db"
baseUrl = "http://ec2-35-178-146-200.eu-west-2.compute.amazonaws.com/"

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
    print(data[0][1])
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

    mycursor.execute("SELECT Class,PY FROM PyList")
    
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
    conn = mysql.connection
mycursor = conn.cursor()

    mycursor.execute("SELECT CutOffTime FROM oodSetup")
    
    now = datetime.now()

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

    
    

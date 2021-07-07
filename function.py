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
app.config['MYSQL_DATABASE'] = 'dorchester_testing'
app.config['MYSQL_HOST'] = '127.0.0.1'
mysql = MySQL()

#dbPath = "/home/ubuntu/Sailing-Manager/DSC.db"
baseUrl = "https://racing.dorchestersailingclub.org.uk/"

def boattoID(boatname):
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)
    print(boatname)
    mycursor.execute("SELECT ID FROM pylist where Class=%s",(boatname))
    data = mycursor.fetchall()
    return data        

def entrylist():
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("SELECT competitors.ID, competitors.Name, competitors.Crew, competitors.SailNum, pylist.Class FROM competitors INNER JOIN pylist ON competitors.BoatID = pylist.ID ") #INNER JOIN pylist ON competitors.ID = pylist.ID
    data = mycursor.fetchall()
    return data

def startTimeList(racelen = 40): #not needed for handicap racing
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("SELECT DISTINCT competitors.BoatID, pylist.PY FROM competitors INNER JOIN pylist ON competitors.BoatID=pylist.ID ORDER BY pylist.PY DESC")
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
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("SELECT * FROM PyList ORDER BY Class")
    
    rawboatList = mycursor.fetchall()
    #print(rawboatList)
    """for items in rawboatList:
        boatList.append(items[0])   
    print(boatList)
    """
    return rawboatList

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def outOftimeSignUp():
    
    now = datetime.now()

    if now.weekday() == 6:
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

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
    mycursor = conn.cursor(buffered=True)
    mycursor.execute("SELECT raceType FROM racesconfig")
    data = mycursor.fetchone()
    return data 

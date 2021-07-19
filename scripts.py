import requests
import csv
import smtplib, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime,timedelta
import os
import mysql.connector
from function import getRaceType, getStartTime
import json
from dbConn import *

mydb = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database=MYSQL_DATABASE
)

for raceid in [1,2]:
    raceID=raceid
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT raceType FROM racesconfig")
    data = mycursor.fetchone()
    raceType = data[0]

    mycursor.execute("SELECT startTime FROM racesconfig where raceID = %s", (raceID,)) #INNER JOIN pylist ON competitors.ID = pylist.ID
    data = mycursor.fetchone()
    getStartTime = data[0]

    if raceType == "PURSUIT":
        #mycursor.execute("SELECT `Name`, `Crew`, `SailNum`,`BoatID`, FROM `Racers` WHERE `FinishedR"+raceid+"` != 0 ORDER BY StateR"+raceid+", `LapsR"+raceid+"` DESC,`TimeFinishedR"+raceid+"` ASC")
        mycursor.execute("SELECT competitors.Name, competitors.Crew, competitors.SailNum, BoatID,races.lapsComplete, races.finTime, races.status FROM races INNER JOIN competitors ON competitors.ID = races.competitorID WHERE races.raceID = %s ORDER BY status, races.lapsComplete DESC, finTime ASC",(raceid,)) #WHERE races.raceID = %s",(raceid,)
        results = mycursor.fetchall()
    else:
        mycursor.execute("SELECT competitors.Name, competitors.Crew, competitors.SailNum, BoatID,races.lapsComplete, races.finTime, races.status, pylist.PY, pylist.Class FROM races INNER JOIN competitors ON competitors.ID = races.competitorID INNER JOIN pylist ON competitors.BoatID = pylist.ID WHERE races.raceID = %s AND races.status = 'FIN'",(raceid,))
        results = mycursor.fetchall()
        mycursor.execute("SELECT lapsComplete FROM races WHERE status='FIN' AND raceID=%s ORDER BY lapsComplete DESC LIMIT 1"%(raceid,))
        try:
            mostLaps = mycursor.fetchone()[0]
        except:
            mycursor.fetchone()
        startTime = getStartTime
        resultsList = []
        for result in results:
            resultsObj = {"name":result[0],"crewName":result[1],"sailNo":result[2],"lapsComplete":result[4],"finTime":result[5],"status":result[6], "py":result[7],"class":result[8]}
            resultsObj['elapsedTimeSeconds'] = int(resultsObj['finTime']-startTime)
            resultsObj['correctedTimeSeconds'] = int(((resultsObj['elapsedTimeSeconds']*mostLaps*1000)/(resultsObj['py']*resultsObj['lapsComplete'])))     # (Elapsed time x most laps x 1000) / (PN x actual laps)
            resultsObj['elapsedTime'] = str(timedelta(seconds=resultsObj['elapsedTimeSeconds']))
            resultsObj['correctedTime'] = str(timedelta(seconds=resultsObj['elapsedTimeSeconds']))
            resultsList.append(resultsObj)
        resultsListSorted = sorted(resultsList, key=lambda k: k['correctedTime']) 

        keys = resultsListSorted[0].keys()
        csvList = []
        csvList.append(list(keys))
        for competitor in resultsListSorted:
            tempList = []
            for key in keys:
                tempList.append(str(competitor[key]))
            csvList.append(tempList)
        
    #Generate csv file
    with open('race%s.csv'%(raceid,), 'w', newline='') as f:
        writer = csv.writer(f)
        for row in csvList:
            writer.writerow(row)

    gmail_user = 'raceresults@dorchestersailingclub.org.uk'
    gmail_password = '+p@8Zf9}~ji2'

    sent_from = 'Dorchester Sailing Club <%s>'%(gmail_user,)
    body = 'Find attached results for race %s'%(raceid, )

    message = MIMEMultipart()
    message["From"] = gmail_user
    message["To"] = 'raceresults@dorchestersailingclub.org.uk'
    message["Subject"] = 'Results from race %s - %s'%(raceid, datetime.now().strftime("%d %b %Y"))


    message.attach(MIMEText(body, "plain"))

    filename = 'race%s.csv'%(raceid,)

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        "attachment; filename=%s race %s.csv"%(datetime.now().strftime("%Y-%m-%d"),raceid),
    )

    message.attach(part)
    text = message.as_string()

    try:
        server = smtplib.SMTP_SSL('smtp.dorchestersailingclub.org.uk', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, message["To"], text)
        server.close()
        print('Email sent!')
        # ...send emails
    except Exception as e: 
        print(e)
    
    if os.path.exists(filename):
        os.remove(filename)
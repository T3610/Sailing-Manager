import requests
import csv
import smtplib, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
for raceid in [1,2]:
    #Gets the json data from server
    url = "http://127.0.0.1:5000/resultsJSON/%s"%(raceid,)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    responseJSON = response.json()
    print(responseJSON)

    #Generate csv file
    with open('race%s.csv'%(raceid,), 'w', newline='') as f:
        writer = csv.writer(f)
        for row in responseJSON:
            writer.writerow(row)



    gmail_user = 'dsc.race.results@gmail.com'
    gmail_password = 'a9piyMZpvZ6bjz'

    sent_from = gmail_user
    body = 'Find attached results for race %s'%(raceid, )

    message = MIMEMultipart()
    message["From"] = gmail_user
    message["To"] = 'dsc.race.results@gmail.com'
    message["Subject"] = 'Today\'s results from race %s'%(raceid, )


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
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, message["To"], text)
        server.close()
        print('Email sent!')
        # ...send emails
    except:
        print('Something went wrong...')
    
    if os.path.exists(filename):
        os.remove(filename)
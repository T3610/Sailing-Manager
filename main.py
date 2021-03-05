from function import *

DEBUG = True
app = Flask(__name__)

#app.run(host='0.0.0.0')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/startingorder')
def startingorder():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT RaceLen FROM oodSetup")
    data = mycursor.fetchall()
    print(data[0][0])
    return render_template('startingorder.html',data = startTimeList(data[0][0])[0])

@app.route('/signup')
def signup():
    if outOftimeSignUp(): #if end of signup period has not passed
        return render_template('entryForm.html',boat =boats())
    else:
        return "Last Sign up Time Has Passed, Please Speak to the OOD",400

@app.route('/oodsignup')
def oodsignup():
    return render_template('entryForm.html',boat =boats())

@app.route('/')
def index():
    return render_template('index.html',onTime = outOftimeSignUp())

@app.route('/startTime')
def starttime():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT cutofftime FROM oodSetup")
    
    data = mycursor.fetchone()
    print(data)

    return data[0]

@app.route('/oodracesetup', methods=["GET","POST"])
def oodracesetup():
    if request.method == 'POST':
        print(request.form)
        #print(request.form["racelen"],request.form["cutofftime"])
        mycursor = mydb.cursor()

        mycursor.execute("UPDATE oodSetup SET CutOffTime=?, RaceLen=? WHERE RaceLen IS NOT NULL",(request.form["CutOffTime"],request.form["RaceLen"],0))
        mydb.commit()
        return redirect('/oodracesetup')
    elif request.method == 'GET':
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM oodSetup")
        
        data = mycursor.fetchone()
        #print(data)

        return render_template('oodracesetup.html', racelen = data[1], lastentry = data[0],  entries=entrylist(), timings = startTimeList(data[1])[0], empty = startTimeList(data[1])[1])


@app.route('/editentry/<id>', methods=["POST"])
def updateentry(id):
    if request.method == 'POST':
        formData = []
        #print(request.form)
        formData = request.form["name"],request.form["Cname"],request.form["sailNum"],request.form["class"]
        #print(formData[0])
        mycursor = mydb.cursor()
        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE  Racers SET name=?,Crew=?,SailNum=?,Boat=? WHERE ID=?",(formData[0],formData[1],formData[2],formData[3],id))

        # Save (commit) the changes
        mydb.commit()
        #print(request.form)
    
        return redirect("/oodracesetup")

@app.route('/entries', methods=["GET","POST"])
def form(id=0):
    if request.method == 'POST':
        formData = []
        #print(request.form)
        formData = request.form["name"],request.form["Cname"],request.form["sailNum"],request.form["class"]
        #print(formData[0])
        mycursor = mydb.cursor()
        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("INSERT INTO Racers (Name,Crew,SailNum,Boat) values (%s,%s,%s,%s)",(formData[0],formData[1],formData[2],formData[3]))

        # Save (commit) the changes
        mydb.commit()
        #print(request.form)
    
        return redirect("/entries")
        
    elif request.method == 'GET':
        return render_template('entryList.html', data=entrylist())
    else:  
        return 'Use POST or GET', 405

@app.route('/deleteentry/<id>')
def deleteentry(id):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM Racers WHERE ID=?",(id))
    mydb.commit()
    return redirect("/oodracesetup")

@app.route('/editentry/<id>')
def editentry(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Racers WHERE ID=?",(id))
    entry = mycursor.fetchone()
    return render_template('entryEdit.html',boat =boats(),id=entry[0], name=entry[1], cName=entry[2], sailNo=entry[3], currentBoat=entry[4])

@app.route('/pylist')
def editpylist():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pylist")
    pylist = mycursor.fetchall()
    return render_template('pylist.html',pylist=pylist)     

@app.route('/pyedit/<id>')
def editpy(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pylist WHERE ID=?",(id))
    entry = mycursor.fetchone()
    return render_template('pyEdit.html',id=entry[0], boat=entry[1], py=entry[2])


@app.route('/editpy/<id>', methods=["POST"])
def updatepy(id):
    if request.method == 'POST':
        formData = []
        #print(request.form)
        formData = request.form["Bname"],request.form["PY"]
        #print(formData[0])
        mycursor = mydb.cursor()
        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE  pylist SET Class=?,PY=? WHERE ID=?",(formData[0],formData[1],id))

        # Save (commit) the changes
        mydb.commit()
        #print(request.form)
    
        return redirect("/pylist")

@app.route('/deletepy/<id>')
def deletepy(id):
    print(id)
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM pylist WHERE ID=?",(id,))
    mydb.commit()
    return redirect("/pylist")

@app.route('/addpy', methods=["GET","POST"])
def addpy():
    if request.method == 'POST':
        formData = []
        #print(request.form)
        formData = request.form["Bname"],request.form["PY"]
        #print(formData[0])
        mycursor = mydb.cursor()
        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("INSERT INTO pylist (Class,PY) values (?,?)",(formData[0],formData[1]))
        
        # Save (commit) the changes
        mydb.commit()
        return redirect("/pylist")
    elif request.method == 'GET':
        return render_template("pyadd.html")

@app.route('/enterresults')
def enterresults():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Racers")
    entries = mycursor.fetchall() #id, Helm, Crewname, Sail Num, Class
    print(entries)

    mycursor.execute("SELECT laps FROM oodSetup")
    data = mycursor.fetchone()
    
    return render_template("enterresults.html", entries=entries) 




#MAKE SURE AT END
if __name__ == '__main__':
    print("hi")
    app.run(host="0.0.0.0", port=3000)
 
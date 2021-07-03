from function import *

DEBUG = True

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

username = 'DSC-OOD'

users = {username:{'pw':'laser'}}

class User(UserMixin):
  pass

@login_manager.user_loader
def user_loader(username):
  if username not in users:
    return

  user = User()
  user.id = username
  return user

@login_manager.request_loader
def request_loader(request):
  username = request.form.get('username')
  if username not in users:
    return

  user = User()
  user.id = username

  user.is_authenticated = request.form['pw'] == users[username]['pw']

  return user



@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    if request.form.get('pw') == users[username]['pw']:
      user = User()
      user.id = username
      flask_login.login_user(user)
      return redirect(url_for('oodracesetup'))
  return render_template('login.html')

@app.route('/logout')
def logout():
  flask_login.logout_user()
  return redirect('/')

#app.run(host='0.0.0.0')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/startingorder')
def startingorder():
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("SELECT raceLen FROM racesconfig")
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
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("SELECT cutOffTime FROM racersconfig")
    
    data = mycursor.fetchone()
    print(data)

    return str(data[0])

@app.route('/oodracesetup', methods=["GET","POST"])
@flask_login.login_required
def oodracesetup():
    if request.method == 'POST':
        #print(request.form)
        #print(request.form["racelen"],request.form["cutofftime"])
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)


        mycursor.execute("UPDATE racesconfig SET cutOffTime=%s, raceLen=%s, raceType=%s ",(request.form["cutofftime"],request.form["racelen"],request.form["raceType"].upper()))
        conn.commit()
        return redirect('/oodracesetup')
    elif request.method == 'GET':
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        mycursor.execute("SELECT DATE_FORMAT(CutOffTime, '%H:%i'), raceLen, raceType FROM racesconfig")
        
        data = mycursor.fetchone()
        #print(data)
        return render_template('oodracesetup.html', racelen = data[1], lastentry = data[0], racetype = data[2], entries=entrylist(), timings = startTimeList(data[1])[0], empty = startTimeList(data[1])[1])


@app.route('/editentry/<id>', methods=["POST"])
def updateentry(id):
    if request.method == 'POST':
        formData = []
        #print(request.form)
        formData = request.form["name"],request.form["Cname"],request.form["sailNum"],request.form["class"]
        #print(formData[0])
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE  competitors SET name=%s,Crew=%s,SailNum=%s,Boat=%s WHERE ID=%s",(formData[0],formData[1],formData[2],formData[3],id))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return redirect("/oodracesetup")

@app.route('/entries', methods=["GET","POST"])
def form(id=0):
    if request.method == 'POST':
        formData = []
        
        formData = [request.form["name"],request.form["Cname"],request.form["sailNum"],request.form["class"]]
        print(formData)
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("INSERT INTO competitors (Name,Crew,SailNum,BoatID) values (%s,%s,%s,%s)",(formData[0],formData[1],formData[2],formData[3]))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return redirect("/entries")
        
    elif request.method == 'GET':
        return render_template('entryList.html', data=entrylist())
    else:  
        return 'Use POST or GET', 405

@app.route('/deleteentry/<id>')
def deleteentry(id):
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("DELETE FROM competitors WHERE ID=%s",(id,))
    conn.commit()
    return redirect("/oodracesetup")

@app.route('/editentry/<id>')
def editentry(id):
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("SELECT * FROM Racers WHERE ID=%s",(id,))
    entry = mycursor.fetchone()
    return render_template('entryEdit.html',boat =boats(),id=entry[0], name=entry[1], cName=entry[2], sailNo=entry[3], currentBoat=entry[4])

@app.route('/pylist')
@flask_login.login_required
def editpylist():
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("SELECT * FROM PyList")
    pylist = mycursor.fetchall()
    return render_template('pylist.html',pylist=pylist)     

@app.route('/results/<raceid>')
def results(raceid):
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("SELECT `Name`, `Crew`, `SailNum`,`Boat`,StateR"+raceid+" FROM `Racers` WHERE `FinishedR"+raceid+"` != 0 ORDER BY StateR"+raceid+", `LapsR"+raceid+"` DESC,`TimeFinishedR"+raceid+"` ASC")
    results = mycursor.fetchall()
    return render_template('results'+raceid+'.html',results=results)     

@app.route('/results')
def resultsRedirect():
    return redirect("/results/1")

@app.route('/pyedit/<id>')
def editpy(id):
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("SELECT * FROM PyList WHERE ID=%s",(id,))
    entry = mycursor.fetchone()
    return render_template('pyEdit.html',id=entry[0], boat=entry[1], py=entry[2])


@app.route('/editpy/<id>', methods=["POST"])
def updatepy(id):
    if request.method == 'POST':
        formData = []
        print(request.form)
        formData = request.form["Bname"],request.form["PY"]
        #print(formData[0])
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE  PyList SET Class=%s,PY=%s WHERE ID=%s",(formData[0],formData[1],id))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return redirect("/pylist")

@app.route('/deletepy/<id>')
def deletepy(id):
    #print(id)
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("DELETE FROM PyList WHERE ID=%s",(id,))
    conn.commit()
    return redirect("/pylist")

@app.route('/addpy', methods=["GET","POST"])
def addpy():
    if request.method == 'POST':
        formData = []
        #print(request.form)
        formData = request.form["Bname"],request.form["PY"]
        #print(formData[0])
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("INSERT INTO PyList (Class,PY) values (%s,%s)",(formData[0],formData[1]))
        
        # Save (commit) the changes
        conn.commit()
        return redirect("/pylist")
    elif request.method == 'GET':
        return render_template("pyadd.html")

@app.route('/enterresults')
@flask_login.login_required
def enterresults():
    return redirect("/enterresults/1") 

@app.route('/enterresults/1')
@flask_login.login_required
def enterresultsR1():
    return render_template("enterresults1.html") 

@app.route('/enterresults/2')
@flask_login.login_required
def enterresultsR2():
    return render_template("enterresults2.html")

@app.route('/api/results/<raceid>', methods=["GET"])
def resultsAPI(raceid):
    if request.method == 'GET':
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("SELECT Racers.* FROM Racers INNER JOIN PyList ON Racers.Boat = PyList.Class WHERE StateR"+raceid+" IN ('0', 'FIN') ORDER BY FinishedR"+raceid+" ,LapsR"+raceid+" ASC, LatestLapRoundingR"+raceid+", PyList.PY DESC, Name")
        entries = mycursor.fetchall()
        entriesJSON = json.dumps(entries)
    
        return entriesJSON

@app.route('/addlap/<raceid>/<id>', methods=["PATCH"])
def addlap(raceid,id):
    if request.method == 'PATCH':
        lapTime = request.args.get('lapTime')
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE Racers SET LapsR"+raceid+" = LapsR"+raceid+" + 1, LatestLapRoundingR"+raceid+" = %s WHERE ID=%s",(lapTime, id,))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return "success",204

@app.route('/removelap/<raceid>/<id>', methods=["PATCH"])
def removelap(raceid,id):
    if request.method == 'PATCH':
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE Racers SET LapsR"+raceid+" = LapsR"+raceid+" - 1 WHERE ID=%s AND LapsR"+raceid+" >0",(id,))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return "success",204

@app.route('/finish/<raceid>/<id>', methods=["PATCH"])
def finish(raceid,id):
    if request.method == 'PATCH':
        finishTime = request.args.get('finishTime')

        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE Racers SET FinishedR"+raceid+" = 1, TimeFinishedR"+raceid+" = %s, StateR"+raceid+" = %s WHERE ID=%s",(finishTime, "FIN", id))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return "success",204

@app.route('/unfinish/<raceid>/<id>', methods=["PATCH"])
def unfinish(raceid,id):
    if request.method == 'PATCH':
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE Racers SET FinishedR"+raceid+" = 0, TimeFinishedR"+raceid+" = 0, StateR"+raceid+" = %s WHERE ID=%s",("0",id))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return "success",204

@app.route('/finishbefore/<raceid>/<id>', methods=["PATCH"])
def finishbefore(raceid,id):
    if request.method == 'PATCH':
        finishTime = request.args.get('finishTime')

        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE Racers SET FinishedR"+raceid+" = 1, LapsR"+raceid+" = LapsR"+raceid+" + 1,  TimeFinishedR"+raceid+" = %s , StateR"+raceid+" = %s WHERE ID=%s",(finishTime, "FIN", id))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return "success",204

@app.route('/unfinishbefore/<raceid>/<id>', methods=["PATCH"])
def unfinishbefore(raceid,id):
    if request.method == 'PATCH':
        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE Racers SET FinishedR"+raceid+" = 0 , LapsR"+raceid+" = LapsR"+raceid+" - 1, TimeFinishedR"+raceid+" = 0, StateR"+raceid+" = %s WHERE ID=%s",("0", id,))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return "success",204


@app.route('/retire/<raceid>/<id>', methods=["PATCH"])
def retire(raceid,id):
    if request.method == 'PATCH':

        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE Racers SET FinishedR"+raceid+" = 1, TimeFinishedR"+raceid+" = 0, StateR"+raceid+" = %s WHERE ID=%s",("RET", id))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return "success",204

@app.route('/DNS/<raceid>/<id>', methods=["PATCH"])
def DNS(raceid,id):
    if request.method == 'PATCH':

        conn = mysql.connection
        mycursor = conn.cursor(buffered=True)

        #print(formData[0],formData[1],formData[2],formData[3])
        mycursor.execute("UPDATE Racers SET FinishedR"+raceid+" = 0, TimeFinishedR"+raceid+" = 0, StateR"+raceid+" = %s WHERE ID=%s",("DNS", id))

        # Save (commit) the changes
        conn.commit()
        #print(request.form)
    
        return "success",204

@app.route('/clearAllEntries')
def clearAllEntries():
    conn = mysql.connection
    mycursor = conn.cursor(buffered=True)

    mycursor.execute("DELETE FROM Racers")
    conn.commit()

    return redirect("/oodracesetup")

@app.route('/enterresults/1H')
def enterresults1H():
    return render_template("enterresults1H.html")

#MAKE SURE AT END
if __name__ == '__main__':

    app.run(host="0.0.0.0", port=3000)
 
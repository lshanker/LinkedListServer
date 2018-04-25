from flask import Flask
from flask import request, session
import smtplib
import json
import pyrebase
import time
from email.mime.text import MIMEText

app = Flask(__name__)
config = {
    "apiKey": "AIzaSyCCkJ9iS47Kv54p8NXHNZS5KqBL0S1IkLk",
    "authDomain": "linkedlist-64b5a.firebaseapp.com",
    "databaseURL": "https://linkedlist-64b5a.firebaseio.com",
    "storageBucket": "linkedlist-64b5a.appspot.com",
}
isUndo = False
app.secret_key = '\rhj\xe5\x97\xeb\x17\xea\xb6p\xfd\x8b\x81n[\xba\xa7\\d\x0fu\x92\xe5\x85'
@app.route('/')
def hello_world():
    return 'Hello, World!'
@app.route('/mail', methods=['GET'])
def mail():
 #   session['undo'] = False
    #eStatic Auth stuff
    gmail_user = 'linkedlistemails@gmail.com'  
    gmail_password = 'linkedlist18'
    #List name
    mailList = request.args.get('list')
    #Firebase auth and recipient generation
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("hgsata@gmail.com", "testuser")
    db = firebase.database()
    res = db.child("lists").order_by_key().equal_to(mailList).get()
    vals = res.val()
    x = list(vals[mailList]['members'].items())
    recipients = list()
    for i in x:
        print(i[1]['email'])
        recipients.append(i[1]['email'])
    #TLS handshake with GMAIL
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(gmail_user, gmail_password)
    
    for pers in recipients:
       
        msg = MIMEText(request.args.get('message') + '\n<a href=\"http://hareeshgali.asuscomm.com/unsub?list=' +mailList +'&email='+ pers +'\">Unsubscribe from this list </a>', 'html')
        msg['Subject'] = request.args.get('subj')
        msg['From'] = "linkedlistemails@gmail.com"
        msg['To'] = pers
        s.sendmail( "linkedlistemails@gmail.com", pers, msg.as_string())
    
   
    s.close()
    
    return "gfdsg", 200

@app.route('/sub', methods=['GET'])
def add():
    mailList = request.args.get('list')
    email = request.args.get('email')
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    
    user = auth.sign_in_with_email_and_password("hgsata@gmail.com", "testuser")
    db = firebase.database()
    data = json.dumps(email)
    db = firebase.database()
    lname = db.child("lists").child(mailList).child("name").get()
    lname = lname.val()
    res = db.child("lists").child(mailList).child("members").get()
    count = 0
    if(res is None):
        for i in res.each():
            if(i.val() == email):
                count = count + 1

    
    name = db.child("lists").child(mailList).child("name").get()
    name = name.val()
    resf = db.child("users").get()
    vals = resf.val()
    #print(vals)
    #x = list(vals[mailList]['members'].items())
    rem = ""
    shit = list()
    for i in vals:
        shit.append(i)
    for i in range(len(vals)):
        print(vals[shit[i]]['email'])
        if(vals[shit[i]]['email'] == email):
            rem = shit[i]
            break
   
    if(count == 0):
        data = {mailList : lname}
        data2 = {
                "email" : email,
                "isMod" : False
                }
        db.child("users").child(rem).child("lists").update(data)
        db.child("lists").child(mailList).child("members").push(data2)
        return "ok"
    
    return "gfdsg"
@app.route('/uniqueList', methods=['GET'])
def uniqCheck():
    listName = request.args.get('list')
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("hgsata@gmail.com", "testuser")
    db = firebase.database()
    res = db.child("lists").order_by_key().equal_to(listName).get()
    count = 0
    for i in res.each():
        count = count + 1
    # print(count)
    if(count == 0):
        return "OK", 200
    else:
        return "NOT OK", 406
    return res
@app.route('/unsub', methods=['GET'])
def delete():
    mailList = request.args.get('list')
    email = request.args.get('email')
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("hgsata@gmail.com", "testuser")
    db = firebase.database()
    res = db.child("lists").order_by_key().equal_to(mailList).get()
    
    keys = res.key()
    print(keys)
    vals = res.val()
    x = vals[mailList]['members'].items()
    rem = ""
    print(x)
    for key, i in x:
        print(i['email'])
        if(i['email'] == email):
            rem = key
            break
    if(rem != ""):
        db.child("lists").child(mailList).child("members").child(rem).remove()
    
    res = db.child("users").get()
    
    keys = res.key()
    print(keys)
    vals = res.val()
    print(vals)
    #x = vals[mailList]['members'].items()
    rem = ""
    #print(x)
    for key, i in vals.items():
        print(i['email'])
        if(i['email'] == email):
            print(key)
            rem = key
            break
    if(rem != ""):
        db.child("users").child(rem).child("lists").child(mailList).remove()
    



    return "OK"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


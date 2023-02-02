from flask import Flask,render_template,redirect,request,session
from pymongo import MongoClient
import hashlib
from bson.objectid import ObjectId

client=MongoClient('localhost',27017)
db=client['B2']
c_register=db['register']
c_data=db['data']

app=Flask(__name__)
app.secret_key='b2sacet'

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/dashboard')
def dashboardpage():
    return render_template('dashboard.html')

@app.route('/sender')
def senderpage():
    data=[]
    read_data_register=c_register.find()
    for i in read_data_register:
        dummy=[]
        if i['username']!=session['username']:
            dummy.append(i['username'])
            data.append(i['username'])

    return render_template('sender.html',dashboard_data=data,l=len(data))

@app.route('/receiver')
def receiverpage():
    data=[]
    read_data_hash=c_data.find()
    for i in read_data_hash:
        username=session['username']
        if(i['receiver']==username):
            dummy=[]
            dummy.append(i['username'])
            dummy.append(i['data'])
            dummy.append(i['hash'])
            if(i['hash']==i['rx_hash']):
                dummy.append('Protected')
            else:
                dummy.append('Danger')
            data.append(dummy)

    return render_template('receiver.html',dashboard_data=data,l=len(data))

@app.route('/logout')
def logoutpage():
    session['username']=None
    return redirect('/')

@app.route('/sent')
def sentpage():
    username=session['username']
    data=[]
    read_data_hash=c_data.find()
    for i in read_data_hash:
        if(i['username']==username):
            dummy=[]
            dummy.append(i['receiver'])
            dummy.append(i['data'])
            dummy.append(i['hash'])
            data.append(dummy)

    return render_template('sent.html',dashboard_data=data,l=len(data))

@app.route('/signupform',methods=['post','get'])
def signupform():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    if len(username)==0 or len(password)==0:
        return render_template('index.html',res1='Enter details properly')
    k={}
    k['username']=username
    k['password']=password
    read_data_register=c_register.find()
    for i in read_data_register:
        if i['username']==k['username']:
            return render_template('index.html',res1='Username exist')
    c_register.insert_one(k)
    return render_template('index.html',res='Registered User')

@app.route('/loginform',methods=['post','get'])
def loginform():
    username=request.form['username1']
    password=request.form['password1']
    print(username,password)
    read_data_register=c_register.find()
    for i in read_data_register:
        if i['username']==username and i['password']==password:
            session['username']=username
            return redirect('/dashboard')
            # return render_template('index.html',res4='valid login')
    return render_template('index.html',res3='Invalid login')

@app.route('/senderform',methods=['post','get'])
def senderform():
    data=request.form['data']
    receiver=request.form['receiver']
    print(data,receiver)
    k={}
    k['username']=session['username']
    k['receiver']=receiver
    k['data']=data
    h=hashlib.sha1()
    h.update(data.encode('utf-8'))
    k['hash']=h.hexdigest()
    k['rx_hash']=k['hash']
    read_data_hash=c_data.find()
    for i in read_data_hash:
        if(k['hash']==i['hash'] and i['username']==session['username'] and i['receiver']==k['receiver']):
            data1=[]
            read_data_register=c_register.find()
            for i in read_data_register:
                dummy=[]
                if i['username']!=session['username']:
                    dummy.append(i['username'])
                    data1.append(i['username'])
            return (render_template('sender.html',dashboard_data=data1,l=len(data1),res1='You have already sent'))

    c_data.insert_one(k)
    data=[]
    read_data_register=c_register.find()
    for i in read_data_register:
        dummy=[]
        if i['username']!=session['username']:
            dummy.append(i['username'])
            data.append(i['username'])
    return (render_template('sender.html',dashboard_data=data,l=len(data),res='Data Sent and hash code - '+str(k['hash'])))

@app.route('/alter',methods=['GET','POST'])
def alterdata():
    data=[]
    read_data_hash=c_data.find()
    for i in read_data_hash:
        data.append(i['_id'])

    return render_template('alter.html',dashboard_data=data,l=len(data))

@app.route('/alterform',methods=['GET','POST'])
def alterform():
    dataid=request.form['dataid']
    msg=request.form['msg']
    print(dataid,msg)
    h=hashlib.sha1()
    h.update(msg.encode('utf-8'))
    newhash=h.hexdigest()
    temp=c_data.find({'"_id"':ObjectId(dataid)})
    print(temp)
    for i in temp:
        print(i)
    c_data.update_one({'_id':ObjectId(dataid)},{"$set":{"data":msg,"hash":newhash}})

    data=[]
    read_data_hash=c_data.find()
    for i in read_data_hash:
        data.append(i['_id'])
    return render_template('alter.html',dashboard_data=data,l=len(data),res='Data altered')


if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
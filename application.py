import os, json
from models import *
import queue
from jsonmerge import Merger
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vfemefkkfvpndz:7dda029ddaa79d315de1313328e07ab73277d64e97b5b8e7da7a5b787529f04d@ec2-54-247-103-43.eu-west-1.compute.amazonaws.com:5432/d8qr7lndoqe6lh"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

q1 = queue.Queue(100)

chatlists = [[]]
chatlist = []

chatlistmax = 10
chatmessagemax = 100

db.init_app(app)

@app.route("/")
def index():

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    login_name=request.form.get("login_name")
    password=request.form.get("password")
    user = users.query.filter_by(login_name=login_name,password=password).first()

    if user is None:
        return render_template("login.html", message ="user not found")
    else:
        f = open('datas.json')
        chatdata = json.load(f)
        chatnamelist = chatdata

        message1 = len(chatdata['gold'])

        return render_template("index.html", user=user, chatnamelist=chatnamelist, message1=message1, chatdata=chatdata)


@app.route("/chat/<chat_name>")
def chat(chat_name):
    f = open('datas.json')
    chatdata = json.load(f)

    message1 = chatdata[chat_name]
    return render_template("chat.html", user="test", chat_name=chat_name, chatnamelist=chatdata, message1=message1)



@socketio.on("submit chat")
def vote(data):

    selection = data["selection"]
    message = data["message"]
    loginname = data["loginname"]
    chat_name = data["chat_name"]
    timestamp1 = datetime.datetime.now()
    timestamp=timestamp1.strftime("%c")
    schema = {
            "properties" : {
                chat_name: {
                    "mergeStrategy": "append"
                    }
                }
            }
    merger = Merger(schema)


    with open('datas.json', 'r') as readfile:
        chatdata = json.load(readfile)

    fullcount = len(chatdata[chat_name])
    count=100
    while count < fullcount:
        del chatdata[chat_name][-1]
        count = count + 1

    chatdat = {}
    chatdat[chat_name]=[]
    chatdat[chat_name].append({'chatter':loginname, 'message':message, 'timestamp': timestamp})
    result = merger.merge(chatdat, chatdata)

    with open('datas.json', 'w') as outfile:

        json.dump(result, outfile, indent=4)

    emit("announce vote", {"timestamp": timestamp , "message": message, "loginname": loginname }, broadcast=True)

@app.route("/addroom")
def addroom():
    return render_template("addroom.html")


@app.route("/result", methods=["POST"] )
def result():
    chat_name = request.form.get("chat_room_name")
    name_check = 1
    chatnamelist = {"main" , "blue"}

    schema = {
            "properties" : {
                chat_name: {
                    "mergeStrategy": "append"
                            }
                        }
                }
    merger = Merger(schema)
    chatdat = {}
    chatdat[chat_name]=[]
    with open('datas.json', 'r') as readfile:
            chatdata = json.load(readfile)
    for names in chatdata:
        if names == chat_name:
            name_check = 0
            break
        else:
            name_check = 1

    if name_check == 0:
        return render_template ("error.html", message = "Chat room name has alreade used. Please choose other name")
    else:
        result = merger.merge(chatdat, chatdata)
        with open('datas.json', 'w') as outfile:
            json.dump(result, outfile, indent=4)

            return render_template("error.html",message ="success of chatroom")

@app.route("/logout")
def logout():
    return render_template("login.html")

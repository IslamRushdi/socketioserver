from socket import socket

from flask import Flask, render_template, redirect, request, session


from flask.globals import request
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room

from flask import g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


global my_IDlist
VolID =[];
global Vol
blind =[];
blindSdp =[];
global counter
global ICE


@app.route('/test')
def register():
    return "working!"


@socketio.on('connect')
def test_connect():
    print('Client connected')
    




@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


# @socketio.on('ID to server')
# def handle_message(data):
#     print('received message: ' + data)
#     data = data.split()
#     if(data[1]==0):
#         VolID[counter] = data
#         counter = counter+1


@socketio.on('on offer')
def handle_message(data):
    print('received message: ' + data)
    data = data.split()
    sdpBlind = data[0]
    sdpVol = Vol.pop()
    socketio.emit('','getting Second side SDP of volunteer',sdpVol,'')
    room = session.get('room')
    join_room(room)
    socketio.emit('', 'getting Second side SDP of Blind', data, '',room=VolID[0])
    # request.sid


# def send_message(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     socketio.emit('', 'getting Second side SDP of Blind', data, '')


@socketio.on('get ICE')
def handle_event(data):
    print('received message: ' + data)
    data = data.split()
    ICE = data[0]
    socketio.emit('','getting ICE from blind',ICE, '')

@socketio.on('on answer')
def handle_event(data):
    print('received message: ' + data)
    data = data.split()
    Vol.append(data[0])
    VolID.append(request.sid)



# getting Second side SDP of Blind
# getting Second side SDP of volunteer
# getting ICE from blind





if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True,port=5000)



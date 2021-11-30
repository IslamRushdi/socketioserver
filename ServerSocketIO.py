from socket import socket

from flask import Flask, render_template, redirect, request, session


from flask.globals import request
from flask_socketio import SocketIO, emit, rooms,send
from flask_socketio import join_room, leave_room

from flask import g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


# my_IDlist=None
volunteers_id =[]
volunteers_sdp=dict()
blind =[]
blind_await_ICE=dict()
# counter=None
# ICE=None
room ='volunteers'



@app.route('/test')
def register():
    return "working!"


@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    if request.sid in volunteers_id:
        volunteers_id.remove(request.sid)
        leave_room(room)
        
    print('Client disconnected')


@socketio.on('volunteer: connect to room')
def handle_volunteer_connected():
    volunteers_id.append(request.sid)
    join_room(room)
    
    


@socketio.on('blind: send sdp')
def handle_creating_offer(blind_sdp):
    #blind sdp: string
    print('blind sdp recieved in server')
    # print(blind_sdp)
    if len(volunteers_id) == 0:
        return socketio.emit('server: no volunteer found')
    
    # blind_candidate = blind_connection['candidate']

    blind_data ={
        "sdp":blind_sdp,
        "id": request.sid,
    }

    blind.append(blind_data)
    print(blind_data)
    socketio.emit('server: send blind connection to all volunteers to create offer',blind_data, room = room)
    # socketio.emit('server: send blind connection to all volunteers to create offer',blind_data, broadcast=True)
    # socketio.send('server: send blind connection to all volunteers to create offer',blind_data, to=room)


@socketio.on('volunteer: send sdp, candidate and blind id')
def handle_receiving_volunteer_candidate(volunteer_invitation):
    #volunteer_invitation = {
    #   candidate: dict,
    #   sdp : string,
    #   blindId: string
    # }
    print('volunteer sdp & candidate recieved in server')
    print(volunteer_invitation)

    volunteer_info = {
       "candidate" : volunteer_invitation['candidate'],
       "sdp" : volunteer_invitation['sdp']
    }
    blindId = volunteer_invitation['blindId']
    socketio.emit('server: send volunteer candidate and sdp',volunteer_info, room= blindId )
    
    # send('server: send volunteer candidate and sdp',volunteer_info  ,to=volunteer_invitation["blindId"])
   





if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True, port=5000)






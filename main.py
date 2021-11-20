from flask import Flask, render_template
from flask_socketio import SocketIO

from flask import g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


global my_IDlist
global VolID
global Vol
global counter
global ICE


@app.route('/test')
def register():
    return "working!"


@socketio.on('connect')
def test_connect(auth):
    print('Client connected')
    print(auth.id)



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
    socketio.emit('','getting Second side SDP of Blind',sdpBlind,'')
    socketio.emit('','getting Second side SDP of volunteer',sdpVol,'')



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


# getting Second side SDP of Blind
# getting Second side SDP of volunteer
# getting ICE from blind





if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)



from flask import Flask, current_app
from flask import jsonify, redirect, url_for, escape
from flask import request,  session 
from flask import g as Globals
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
import logging

logging.basicConfig()

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

socketio = SocketIO(app)

app.artist = 0
app.log = {}

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

@app.route('/draw/<room>')
def drawing_room(room):
	session['artist'] = str(app.artist)
	session['room'] = room
	app.artist += 1
	return app.send_static_file('draw.html')

@socketio.on('connect', namespace='/draw_data')
def connect():
	join_room(session['room'])
	if session['room'] not in app.log:
		app.log[session['room']] = []
	for move in app.log[session['room']]:
		emit('server_to_client_move', move, room = session['room'])


@socketio.on('client_to_server_move', namespace='/draw_data')
def received_move(obj):
	move = {'point':obj['point'],'isNew': obj['isNew'],'artist':session['artist']}
	app.log[session['room']].append(move)
	emit('server_to_client_move', move, room = session['room'])

if __name__ == '__main__':
	socketio.run(app)
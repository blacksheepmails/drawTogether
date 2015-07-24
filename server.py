from flask import Flask, current_app
from flask import jsonify, redirect, url_for, escape
from flask import request,  session 
from flask import g as Globals
from flask.ext.socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

socketio = SocketIO(app)

app.artist = 0;

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

@app.route('/draw')
def root():
	print(app.artist)
	session['artist'] = str(app.artist)
	app.artist += 1
	print('here2')
	return app.send_static_file('draw.html')

@socketio.on('client_to_server_move', namespace='/draw_data')
def received_move(obj):
	emit('server_to_client_move', {'point':obj['point'], 'isNew': obj['isNew'], 'artist':session['artist']}, broadcast=True)

if __name__ == '__main__':
	socketio.run(app)
from flask import Flask, render_template
from flask_tor import run_with_tor
from flask_socketio import SocketIO, send
import os

port = run_with_tor()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

active_aliases = set()  # Set to store active aliases
@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('check_alias')
def checkAlias(data):
    alias = data['alias']
    if alias in active_aliases:
        socketio.emit('alias_taken', {'message': 'Alias is already taken. Please try a different alias.'})
    else:
        active_aliases.add(alias)
        socketio.emit('alias_available', {'message': 'Alias available.'})

if __name__ == '__main__':
    app.run(port=port, debug=True)

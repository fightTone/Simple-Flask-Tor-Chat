from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import threading
import time

# Mock implementation of run_with_tor for demonstration
def run_with_tor():
    # Example: Start Tor process and return the port
    try:
        # Your logic to start Tor and get the port
        port = 8080  # Change this based on your logic
        return port
    except Exception as e:
        print(f"Error starting Tor: {e}")
        raise

# Start Tor and get the port
port = run_with_tor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

active_aliases = set()  # Set to store active aliases
connected_clients = set()  # Set to store connected clients

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    connected_clients.add(request.sid)
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    connected_clients.discard(request.sid)
    print(f'Client disconnected: {request.sid}')

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

def print_connected_clients():
    while True:
        print(f'Number of unique clients connected: {len(connected_clients)}')
        time.sleep(5)

if __name__ == '__main__':
    # Start the background thread to print connected clients
    threading.Thread(target=print_connected_clients, daemon=True).start()
    # Use socketio.run() instead of app.run() to ensure SocketIO works properly
    socketio.run(app, port=port, debug=True)

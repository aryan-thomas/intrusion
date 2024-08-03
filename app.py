from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Route to serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Event handler for WebSocket connections
@socketio.on('message')
def handle_message(message):
    print(f'Received message: {message}')
    # Broadcast the message to all connected clients
    emit('message', message, broadcast=True)

# Run the Flask application
if __name__ == '__main__':
    socketio.run(app, debug=True)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pandas as pd
import pickle
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

model = pickle.load(open('model4.pkl', 'rb'))



# Display the extracted row(s)

# Route to serve the HTML file
@app.route('/')
def index():
    df = pd.read_csv('test_data.csv')

# Extract row(s) where the value in a particular column matches a specific value
# Example: Extract rows where the 'Name' column is 'Alice'
    extracted_row = df.sample(n=1)
    data = extracted_row
    return render_template('index.html',data=data.to_json())

# Event handler for WebSocket connections
@socketio.on('message')
def handle_message(finalData):
    

    # Process the header to create the features for the model
    # For example, assuming the header contains a single value in 'exampleKey'
    # Convert this value to a feature vector (modify as needed)
      # Adjust this line based on your model's input requirements

    # Make the prediction
    message = finalData['payload']
    header = finalData['header']

    # Convert header to pandas DataFrame
    header_df = pd.read_json(header)

    # Process the DataFrame to create the features for the model
    # Assuming the model expects specific columns
    features = header_df.values

    # Make the prediction
    prediction = model.predict(features)[0]

    print("attack type is:",prediction)
    print("Received Message :",pd.read_json(finalData['header']))
    # Broadcast the message to all connected clients
    emit('message', finalData, broadcast=True)




# Run the Flask application
if __name__ == '__main__':
    socketio.run(app)

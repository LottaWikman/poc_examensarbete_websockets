import json
import uuid
from channels.generic.websocket import WebsocketConsumer

# Create a dictionary to hold the active connections, shared over all instanses of the class Consumer
active_connections = {}


# Broadcast the progress to all active connections of the WebSocket
def broadcast_progress(message):
    for connection in active_connections.values():
        connection.send(
            text_data=json.dumps(
                {
                    "type": "progress_update",
                    "message": message,
                }
            )
        )


class Consumer(WebsocketConsumer):

    # method for creating the initial connect
    def connect(self):

        # Generate a new string id for each connection
        self.connection_id = str(uuid.uuid4())

        self.accept()

        # Store the connection in the active_connections-dictionary
        active_connections[self.connection_id] = self

        self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "message": "You are now connected to the server via WebSocket!",
                }
            )
        )

    # Handling messages from WebSocket
    def receive(self, text_data):

        data = json.loads(text_data)
        print(f"Received message: {data}")

    # Handle messages that are sent to the consumer
    def send_progress(self, event):

        message = event["message"]

        self.send(
            text_data=json.dumps(
                {
                    "type": "progress_update",
                    "message": message,
                }
            )
        )

    # Remove this connection from the list active_connections
    def disconnect(self, close_code):
        if self.connection_id in active_connections:
            del active_connections[self.connection_id]

import json
import uuid
import os
from channels.generic.websocket import WebsocketConsumer

# Create a dictionary to hold the active connections, shared over all instanses of the class Consumer
active_connections = {}

# Directory to upload files to
UPLOAD_DIRECTORY = "uploaded_files"
# If the directory doesn't exist, create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


# Broadcast the progress to all active connections of the WebSocket
# Adding connection_id to make the broadcasting individual
def broadcast_progress(message, connection_id):
    if connection_id in active_connections:
        active_connections[connection_id].send(
            text_data=json.dumps(
                {
                    "type": "progress_update",
                    "message": message,
                }
            )
        )


class Consumer(WebsocketConsumer):

    def connect(self):
        """Accepts the initial WebSocket handshake and registers the connection"""

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
                    "connection_id": self.connection_id,
                }
            )
        )

    def receive(self, text_data):
        """Handling messages from WebSocket"""

        data = json.loads(text_data)
        print(f"Received message: {data}")

    def receive_bytes(self, bytes_data):
        """Handling incoming files through WebSocket"""

        file_name = f"{uuid.uuid4()}.bin"
        file_path = os.path.join(UPLOAD_DIRECTORY, file_name)

        # "w" stands for "write mode" and means that the file is opened up for writing
        # "b" stands for "binary mode" and means that you can handle binary files (= non-textbased files)
        with open(file_path, "wb") as f:
            f.write(bytes_data)

        self.send(
            text_data=json.dumps(
                {
                    "type": "file_upload_success",
                    "message": f"File uploaded successfully as {file_name}",
                    "file_path": file_path,
                }
            )
        )

    def send_progress(self, event):
        """Handle messages that are sent to the consumer"""

        message = event["message"]

        self.send(
            text_data=json.dumps(
                {
                    "type": "progress_update",
                    "message": message,
                }
            )
        )

    def disconnect(self, close_code):
        """Remove this connection from the list active_connections"""

        if self.connection_id in active_connections:
            del active_connections[self.connection_id]

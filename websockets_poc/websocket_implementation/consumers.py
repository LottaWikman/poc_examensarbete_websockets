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

    def receive(self, text_data=None, bytes_data=None):
        """Handling messages from WebSocket"""

        print("Inuti receive-metoden!")

        if text_data:
            data = json.loads(text_data)

            if data.get("type") == "file_info":
                self.pending_file_info = {
                    "filename": data.get("filename", "unknown"),
                    "size": data.get("size", 0),
                    "content_type": data.get("contentType", "application/octet-stream"),
                }

        elif bytes_data:

            print("Du ska skicka binärdata!")

            try:
                # hasattr means "has attribute" and is a check to see if something has a specific attribute,
                # in this case "pending_file_info"
                if hasattr(self, "pending_file_info"):

                    print("Hittade metadata.")

                    filename = self.pending_file_info.get("filename", "unknown")

                    print(f"filename: {filename}")

                    file_path = os.path.join(UPLOAD_DIRECTORY, filename)

                    # "w" stands for "write mode" and means that the file is opened up for writing
                    # "b" stands for "binary mode" and means that you can handle binary files (= non-textbased files)
                    with open(file_path, "wb") as f:
                        f.write(bytes_data)

                    # Send confirmation to the client
                    self.send(
                        text_data=json.dumps(
                            {
                                "type": "file_upload_success",
                                "message": f"Successfully uploaded {filename}",
                                "file_path": file_path,
                                "filename": filename,
                            }
                        )
                    )

                    # Remove the already used data
                    del self.pending_file_info

                else:

                    print("Hittade ingen metadata, genererar ett nytt filnamn.")

                    filename = f"{uuid.uuid1()}.bin"
                    file_path = os.path.join(UPLOAD_DIRECTORY, filename)

                    # "w" stands for "write mode" and means that the file is opened up for writing
                    # "b" stands for "binary mode" and means that you can handle binary files (= non-textbased files)
                    with open(file_path, "wb") as f:
                        f.write(bytes_data)

                    # Send confirmation to the client
                    self.send(
                        text_data=json.dumps(
                            {
                                "type": "file_upload_success",
                                "message": f"Successfully uploaded {filename}",
                                "file_path": file_path,
                                "filename": filename,
                            }
                        )
                    )

            except Exception as e:
                print(f"Error: {e}")

    def disconnect(self, close_code):
        """Remove this connection from the list active_connections"""

        if self.connection_id in active_connections:
            del active_connections[self.connection_id]

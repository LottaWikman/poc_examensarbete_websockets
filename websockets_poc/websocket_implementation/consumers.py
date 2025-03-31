import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    # method for creating the initial connect
    def connect(self):
        self.accept()
        self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "message": "You are now connected to the server via WebSocket!",
                }
            )
        )

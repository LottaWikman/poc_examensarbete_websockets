// DOM = Document Object Model
// Which makes an HTML-page into an object which you can interact with through an API.
// Get the DOM-element with the right types:
// A constant that will represent the file input element that the user will interact with
var fileInput = document.getElementById("fileInput");
// A constant that will represent the upload button in the HTML document
var uploadButton = document.getElementById("uploadButton");
// A constant that will represent the servers response
var serverResponse = document.getElementById("serverResponse");
// WebSocket connection to the server at the specified url
var socket = new WebSocket("ws://localhost:8000/ws/");
// When the socket is opened to the frontend, it will log a message to the console
socket.onopen = function () {
    console.log("Connected to WebSocket server");
};
// When a message is received through WebSocket, the text will be displayed in the serverResponse-element 
socket.onmessage = function (event) {
    serverResponse.innerText = event.data;
};
// If an error occurs with the WebSocket, the console will log a message "WebSocket Error" followed by the actual error
socket.onerror = function (error) {
    console.error("WebSocket Error", error);
};
// When the WebSocket connection is closed, it will log a message into the console saying that it's closed
socket.onclose = function () {
    console.log("WebSocket connection closed");
};
// Function to send a file through WebSocket
var sendFile = function () {
    // If fileinput is falsy, abort the sending of the file
    if (!fileInput.files || fileInput.files.length === 0) {
        alert("Please select a file first!");
        return;
    }
    // Take the first file that is uploaded
    var file = fileInput.files[0];
    // Create an instance of a FileReader
    var reader = new FileReader();
    // When the file is read, it sends the result through WebSocket and logs a message
    reader.onload = function (event) {
        var _a;
        if (((_a = event.target) === null || _a === void 0 ? void 0 : _a.result) instanceof ArrayBuffer) {
            socket.send(event.target.result);
            console.log("File sent!");
        }
    };
    // Reads the file as raw binary data
    reader.readAsArrayBuffer(file);
};
// Adds an eventlistener to the element uploadButton, and calls the sendFile-method when clicked
uploadButton.addEventListener("click", sendFile);

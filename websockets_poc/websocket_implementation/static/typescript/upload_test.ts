
// DOM = Document Object Model
// Which makes an HTML-page into an object which you can interact with through an API.

// Get the DOM-element with the right types:

// A constant that will represent the file input element that the user will interact with
const fileInput = document.getElementById("fileInput") as HTMLInputElement
// A constant that will represent the upload button in the HTML document
const uploadButton = document.getElementById("uploadButton") as HTMLButtonElement
// A constant that will represent the servers response
const serverResponse = document.getElementById("serverResponse") as HTMLPreElement

// WebSocket connection to the server at the specified url
const socket = new WebSocket("ws://localhost:8000/ws/");


// When the socket is opened to the frontend, it will log a message to the console
socket.onopen = () => {
    console.log("Connected to WebSocket server");
};

// When a message is received through WebSocket, the text will be displayed in the serverResponse-element 
socket.onmessage = (event: MessageEvent) => {
    serverResponse.innerText = event.data;
};

// If an error occurs with the WebSocket, the console will log a message "WebSocket Error" followed by the actual error
socket.onerror = (error: Event) => {
    console.error("WebSocket Error", error);
};

// When the WebSocket connection is closed, it will log a message into the console saying that it's closed
socket.onclose = () => {
    console.log("WebSocket connection closed");
};


// Function to send a file through WebSocket
const sendFile = (): void => {

    // If fileinput is falsy, abort the sending of the file
    if (!fileInput.files || fileInput.files.length === 0) {
        alert("Please select a file first!");
        return
    }

    // Take the first file that is uploaded
    const file = fileInput.files[0];
    // Create an instance of a FileReader
    const reader = new FileReader();

    // When the file is read, it sends the result through WebSocket and logs a message
    reader.onload = (event: ProgressEvent<FileReader>) => {
        if (event.target?.result instanceof ArrayBuffer) {
            socket.send(event.target.result);
            console.log("File sent!");
        }
    };

    // Reads the file as raw binary data
    reader.readAsArrayBuffer(file);
};

// Adds an eventlistener to the element uploadButton, and calls the sendFile-method when clicked
uploadButton.addEventListener("click", sendFile)
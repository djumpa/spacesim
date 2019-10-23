var exampleSocket = new WebSocket("ws://localhost:8765");

exampleSocket.onopen = function (event) {
    exampleSocket.send("Here's some text that the server is urgently awaiting!"); 
  };

  exampleSocket.onmessage = function (event) {
    console.log(event.data);
  }


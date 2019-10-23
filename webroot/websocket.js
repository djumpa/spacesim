var exampleSocket = new WebSocket("ws://localhost:8765");
var ws_data = {};
exampleSocket.onopen = function (event) {
    exampleSocket.send("Here's some text that the server is urgently awaiting!"); 
  };

  exampleSocket.onmessage = function (event) {
    //console.log(event.data);
    ws_data = JSON.parse(event.data)
    //console.log(ws_data[0].position)
  }


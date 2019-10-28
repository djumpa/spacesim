var exampleSocket = new WebSocket("ws://localhost:8765");
var ws_data = {};
var ws_data_hist = [];
const MAX_LINE_ELEMENTS = 600;
var first_ws=false;

exampleSocket.onopen = function (event) {
    exampleSocket.send("Here's some text that the server is urgently awaiting!"); 
  };

  exampleSocket.onmessage = function (event) {
    //console.log(event.data);
    ws_data = JSON.parse(event.data)
    
    if (ws_data_hist.length==0) {
      for (let index = 0; index < ws_data.length; index++) {
        ws_data_hist.push(new Array(MAX_LINE_ELEMENTS).fill(new THREE.Vector3(0,0,0))); 
      }
    }
    
    for (let index = 0; index < ws_data.length; index++) {
      ws_data_hist[index].push(ws_data[index].position);
      if (ws_data_hist[index].length>MAX_LINE_ELEMENTS)
      ws_data_hist[index].shift()
    }
    first_ws=true;
    
  }
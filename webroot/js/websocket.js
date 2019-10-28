var exampleSocket = new WebSocket("ws://localhost:8765");
var ws_data = {};
var ws_data_hist = [];
var ws_hist_inert = [];

const MAX_LINE_ELEMENTS = 600;



var ws_count = 0;
exampleSocket.onopen = function (event) {
  exampleSocket.send("Here's some text that the server is urgently awaiting!");
};

exampleSocket.onmessage = function (event) {
  //init
  ws_data = JSON.parse(event.data)
  if (ws_hist_inert.length == 0) {
      for (let index = 0; index < ws_data.length; index++) {
      ws_hist_inert.push(new Array(MAX_LINE_ELEMENTS).fill([0, 0, 0]));
      ws_data_hist.push(new Array(MAX_LINE_ELEMENTS).fill([0, 0, 0]));
    }
  }

  //history logging
  if (ws_count % 1 == 0) {
    for (let index = 0; index < ws_data.length; index++) {
      if (index==3) {
        var tmp = []
        for (let i = 0; i < ws_data[index].position.length; i++) {
          tmp[i] = ws_data[index].position[i]-ws_data[1].position[i];      
        }
       
        ws_hist_inert[index].push(tmp);
      } else {
        ws_hist_inert[index].push(ws_data[index].position);
      }
      
      if (ws_hist_inert[index].length > MAX_LINE_ELEMENTS)
      ws_hist_inert[index].shift()
    }

    
    for (var i = 0; i < MAX_LINE_ELEMENTS; i++) {
  
        ws_data_hist[3][i] = ws_hist_inert[3][i].map(function (num, idx) {
          return num + ws_data[1].position[idx];
        });
        //console.log("start")
        //console.log(ws_hist_inert[3][index][j])

        //console.log(ws_data_hist[3][index][j])
        //ws_data_hist[0][i][j] = ws_hist_inert[0][i][j];
        ws_data_hist[1][i] = ws_hist_inert[1][i].slice();
        ws_data_hist[2][i] = ws_hist_inert[2][i].slice();
      
    }
    

    ws_count = 0;
  }
  
  
  ws_count += 1;
}
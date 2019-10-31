var exampleSocket = new WebSocket("ws://localhost:8765");
var ws_data = {};
var ws_data_hist = [];
var ws_hist_inert = [];

const MAX_LINE_ELEMENTS = 6000;



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

  var sc_velocity = []
  var sc_position = []
  for (let index = 0; index < 3; index++) {
    sc_velocity[index] = ws_data[1].velocity[index] - ws_data[3].velocity[index];
    sc_position[index] = ws_data[1].position[index] - ws_data[3].position[index];
  }
  var sc_vel_mag = Math.round(Math.sqrt(Math.pow(sc_velocity[0],2)+Math.pow(sc_velocity[1],2)+Math.pow(sc_velocity[2],2)))
  var sc_pos_mag = Math.round(Math.sqrt(Math.pow(sc_position[0],2)+Math.pow(sc_position[1],2)+Math.pow(sc_position[2],2)))


  $('.pos').text(Math.round(sc_pos_mag/1000)+"/"+Math.round(sc_pos_mag/1000-6371));
  $('.vel').text(sc_vel_mag);
  $('.e').text(Math.round(ws_data[3].orb.e*1000)/1000);
  $('.a').text(Math.round(ws_data[3].orb.a)/1000);
  $('.i').text(Math.round(ws_data[3].orb.i*10)/10);
  $('.omega').text(Math.round(ws_data[3].orb.omega*10)/10);
  $('.capital-omega').text(Math.round(ws_data[3].orb.argp*10)/10);
  $('.nu').text(Math.round(ws_data[3].orb.nu*10)/10);

  var periapsis = (1-ws_data[3].orb.e)*ws_data[3].orb.a
  var apoapsis = (1+ws_data[3].orb.e)*ws_data[3].orb.a
  $('.pe').text(Math.round(periapsis/1000)+ "/" + +Math.round(periapsis/1000-6371));
  $('.ap').text(Math.round(apoapsis/1000)+ "/" + +Math.round(apoapsis/1000-6371));
  //console.log(ws_data_hist[3][ws_data_hist[3].length-1].position)
  
  ws_count += 1;
}
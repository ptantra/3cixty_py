var mraa = require('mraa');
var dgram = require('dgram');
var client = dgram.createSocket('udp4');

console.log('MRAA Version: ' + mraa.getVersion()); 

var myOnboardLed = new mraa.Gpio(13); 
myOnboardLed.dir(mraa.DIR_OUT); 
var ledState = true; 

var light_sensor=new mraa.Aio(0);
var temp_sensor=new mraa.Aio(1);
var sound_sensor=new mraa.Aio(3);

periodicActivity(); 

function periodicActivity()
{
    
      
  myOnboardLed.write(ledState?1:0);
  ledState = !ledState; 

  var light_val=light_sensor.read();
  var temp_val=temp_sensor.read();
  var sound_val=sound_sensor.read();
    
  send_data("light",light_val);
  send_data("temperature", temp_val);
  send_data("sound", sound_val);
    
  console.log("Temp:"+temp_val+" Light:"+light_val+" Sound:" +sound_val);
    
  setTimeout(periodicActivity,1000);
}

function send_data(x,y){

    var msg = JSON.stringify({
        n: x,
        v: y,
    });

    var sentMsg = new Buffer(msg);
    console.log("Data Sent: " + sentMsg);
    client.send(sentMsg, 0, sentMsg.length, 41234, "127.0.0.1");
    
}
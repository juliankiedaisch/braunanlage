  var ws = new WebSocket('ws://127.0.0.1:8888/ws');
    var $message = $('#message_server');
    var $clock = $('#server_clock');
    var $temp_up = $('#temp_up');
    var $temp_down = $('#temp_down');

    ws.onopen = function(){
      $message.attr("class", 'label label-success');
      $message.text('Verbunden');
    };
    ws.onmessage = function(ev){
      var json = JSON.parse(ev.data);
      //Clock, Temp
      $clock.attr("class", 'label label-info');
      $clock.text(json.server_clock);
      $temp_up.text(json.temp_up);
      $temp_down.text(json.temp_down);

    };
    ws.onclose = function(ev){
      $message.attr("class", 'label label-important');
      $message.text('Verbindung geschlossen');
    };
    ws.onerror = function(ev){
      $message.attr("class", 'label label-warning');
      $message.text('Fehler!');
    };

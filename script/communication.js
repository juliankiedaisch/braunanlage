
    var ServerConnection = 0;
    /* Verbindung zum Server wird aufgebaut */
    var ws = new WebSocket('ws://192.168.178.39:8888/ws')
    var $message = $('#message_server');
    var $clock = $('#server_clock');
    var $temp_up = $('#temp_up');
    var $temp_down = $('#temp_down');
    var $engine1_position = $('#engine1');

    ws.onopen = function(){
      $message.attr("class", 'label label-success');
      $message.text('Verbunden');
      stopSound();
      /* Notification: */
      noty({
        text: 'Verbindung wurde hergestellt!',
        type: 'success',
        closeWith: ['click'],
        callback: {
          onShow: function() {},
          afterShow: function() {},
          onClose: function() {},
          afterClose: function() {},
          onCloseClick: function() {},
        }
      });
      ServerConnection = 1;
      test_connection(ws);
    };
    ws.onmessage = function(ev){
      var json = JSON.parse(ev.data);
      //Clock, Temp
      $clock.attr("class", 'label label-info');
      $clock.text(json.server_clock);
      $temp_up.text(json.temp_up);
      $temp_down.text(json.temp_down);
      $engine1_position.text(json.engine1);
      ServerConnection = 1;

    };
    ws.onclose = function(ev){
      /* Alarmsound */
      playSound();
      /* Notification: */
      noty({
      	text: 'Verbindung zum RaspberryPi ist abgebrochen! Zum Beenden des Alarms best&auml;ttigen.',
        type: 'error',
        closeWith: ['click'],
        callback: {
          onShow: function() {},
          afterShow: function() {},
          onClose: function() { stopSound();},
          afterClose: function() {},
          onCloseClick: function() {},
        }
      });
      $message.attr("class", 'label label-important');
      $message.text('Verbindung geschlossen');

    };
    ws.onerror = function(ev){
      playSound();
      noty({
      	text: 'Verbindung zum RaspberryPi ist abgebrochen! Es trat ein Fehler beim Server auf. Zum Beenden des Alarms best&auml;ttigen.',
        type: 'error',
        closeWith: ['click'],
        callback: {
          onShow: function() {},
          afterShow: function() {},
          onClose: function() { stopSound();},
          afterClose: function() {},
          onCloseClick: function() {},
        }
      });
      $message.attr("class", 'label label-warning');
      $message.text('Fehler!');
    };

    /* Verbindung bei Stromunterbrechung wird geprueft: */
    function test_connection(server) {
      aktuell = new Date();
        setTimeout( function() {
          if (ServerConnection == 0) {
            playSound();
            /* Notification: */
            noty({
              text: 'Verbindung zum RaspberryPi ist abgebrochen! Grund: Stromausfall beim Server! Sofort zur Brauanlage gehen und Lage checken! Zum Beenden des Alarms best&auml;ttigen.',
              type: 'error',
              closeWith: ['click'],
              callback: {
                onShow: function() {},
                afterShow: function() {},
                onClose: function() { stopSound();},
                afterClose: function() {},
                onCloseClick: function() {},
              }
            });
          } else {
            ServerConnection = 0;
            test_connection(server); }
        }, 2000);
      }
    /* Warnsignal, falls der Server nicht mehr antwortet */
    function playSound(){
      $('#alarmsound').append('<audio autoplay loop><source src="alarm.mp3" type="audio/mpeg"></audio>');
    }
    function stopSound(){
      $('#alarmsound').empty();
    }

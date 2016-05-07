
    var ServerConnection = 0;
    /* Verbindung zum Server wird aufgebaut */
    var ws;
    var $message = $('#message_server');
    var $clock = [$('#server_clock'),$('#server_clock2')];
    var $temp_up = [$('#temp_up')];
    var $temp_down = [$('#temp_down')];
    var $engine1_position = [$('#engine1'),$('#engine1_1')];
    var $engine1_max = [$('#engine1_max'),$('#engine1_max_1')];
    var $engine1_min = [$('#engine1_min'),$('#engine1_min_1')];
    var $engine2_position = [$('#engine2'),$('#engine2_1')];
    var $engine2_max = [$('#engine2_max'),$('#engine2_max_1')];
    var $engine2_min = [$('#engine2_min'),$('#engine2_min_1')];
    //Hier wird alles ueber den Zustand der WebSocketverbindung gehaendelt
    //In [0] wird angegeben ob die Verbindung steht , 1 = Verbunden, 0 = Nicht verbunden
    //In [1] wird der Fehler benannt
    //In [2] wird angezeigt, ob der Fehler zum ersten Mal beim prüfen aufgefallen ist, oder schon zum wiederholten Male (Damit auf den Fehler nicht nochmal hingewiesen werden muss)
    var connection_status = new Object();
    //Verbindung wird initialisiert
    open_connection();
    //Nach 2s wird die Verbindung das erste Mal geprueft
    setTimeout(test_connection, 2000);
//Verbindung zum WebSocket wird aufgebaut
function open_connection() {
    ws = new WebSocket('ws://192.168.178.39:8888/ws');
    ws.onopen = function(){
      if (connection_status.ctype != 1) {
        connection_status.cstatus = 0;
      }
      connection_status.ctype = 1;
      connection_status.cnote = 'Verbunden';
      $message.text(connection_status.cnote);
      ServerConnection = 1;
    };
    ws.onmessage = function(ev){
      var json = JSON.parse(ev.data);
      //Der Inhalt der Message wird an den richtigen empfaenger verteilt
      switch (json.message[0]) {
        case "log_vorgang":
          show_log_vorgang(json.message[1])
          break;
        case "log_liste_full":
          make_log_liste_full(json.message[1]);
          break;
        case "server_clock":
          $.each($clock, function (val, obj) {
            obj.text(json.message[1]);
          });
          break;
        case "temp_down":
          $.each($temp_down, function (val, obj) {
            obj.text(json.message[1]);
          });
          break;
        case "temp_up":
          $.each($temp_up, function (val, obj) {
            obj.text(json.message[1]);
          });
          break;
        case "engine1":
          $.each($engine1_position, function (val, obj) {
            obj.text(json.message[1]);
          });
          break;
        case "engine1_max":
          $.each($engine1_max, function (val, obj) {
            obj.text(json.message[1]);
          });
          break;
        case "engine1_min":
          $.each($engine1_min, function (val, obj) {
            obj.text(json.message[1]);
          });
          break;
          case "engine2":
            $.each($engine2_position, function (val, obj) {
              obj.text(json.message[1]);
            });
            break;
          case "engine2_max":
            $.each($engine2_max, function (val, obj) {
              obj.text(json.message[1]);
            });
            break;
          case "engine2_min":
            $.each($engine2_min, function (val, obj) {
              obj.text(json.message[1]);
            });
            break;
        case "b_biertyp":
          if (json.message[1].length>1) {
            message = new Object()
            message.ctype = json.message[1][1];
            message.cstatus = 0;
            message.cnote = json.message[1][2];
            show_noty(message);
          }
          //Die Selects werden neu gemacht
          make_selects1(json.message[1][0]);
          break;
        case "rezept_liste":
          select_rezepte(json.message[1]);
          break;
        case "b_rezept":
          rezept_einlesen(json.message[1]);
          break;
        //Alle Informationen zum Kallibrieren.
        case "kalibrieren":
          input_kalibrieren(json.message[1]);
      }
      //Da der Server die Systemzeit sekuendlich durgibt, benutze ich ein ausbleiben der Nachricht als Zeichen, dass die Verbindung abgebrochen wird.
      ServerConnection = 1;
    };
    ws.onclose = function(ev){
      if (connection_status.ctype != 0) {
        connection_status.cstatus = 0;
      }
      connection_status.ctype = 0;
      connection_status.cnote = 'Die Verbindung zum Server wurde beendet. Hier klicken um den Alarm auszustellen.';
    };
    ws.onerror = function(ev){
      if (connection_status.ctype != 0) {
        connection_status.cstatus = 0;
      }
      connection_status.ctype = 0;
      connection_status.cnote = 'Es trat beim Server ein Fehler auf. Hier klicken um den Alarm auszustellen.';
    };
  }
    function test_connection() {
      //Verbindung zum Server abgebrochen
      if (ServerConnection == 0) {
        //Unerwarter Abbruch vom Server. Server hat keine Nachricht gesendet
        if (connection_status.ctype != 0) {
          connection_status.cstatus = 0;
          connection_status.cnote = "Warnung! Unerwarteter Verbindungsabbruch!";
          connection_status.ctype = 0;
        }
        //Neue Verbindung wird versucht aufzubauen
        open_connection();
      }
      //Benachrichtigung wird angezeigt
      $message.text(connection_status.cnote);
      //Noty wird geprueft, ob Nachricht schon angezeigt wurde.
      show_noty(connection_status)
      //Variable zur Bestimmung der Verbindung wird zurückgesetzt.
      ServerConnection = 0;
      //Neuausfuehrung der Funktion mit Zeitverzoegerung.
      setTimeout(test_connection, 4000);
    }
    //Hier werden die Notyy erstellt. Mehrmalsnennung bei gleichem Fehler soll verhindert werden.
    function show_noty(cs) {
      //positive Nachricht
      if(cs.ctype==1 && cs.cstatus==0) {
        noty({
          text: cs.cnote,
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
        cs.cstatus = 1;
      }
      //Hugh ErrorMessage
      else if(cs.ctype==0 && cs.cstatus==0) {
        playSound();
        cs.cstatus = 1;
        noty({
          text: cs.cnote,
          type: 'error',
          closeWith: ['click'],
          callback: {
            onShow: function() {},
            afterShow: function() {},
            onClose: function() {stopSound();},
            afterClose: function() {},
            onCloseClick: function() {},
          }
        });
      }
      //Little ErrorMessage
      else if(cs.ctype==2 && cs.cstatus==0) {
        cs.cstatus = 1;
        noty({
          text: cs.cnote,
          type: 'warning',
          closeWith: ['click'],
          callback: {
            onShow: function() {},
            afterShow: function() {},
            onClose: function() {},
            afterClose: function() {},
            onCloseClick: function() {},
          }
        });
      }
    }
    /* Warnsignal, falls der Server nicht mehr antwortet */
    function playSound(){
      $('#alarmsound').append('<audio autoplay loop><source src="alarm.mp3" type="audio/mpeg"></audio>');
    }
    function stopSound(){
      $('#alarmsound').empty();
    }

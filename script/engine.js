/* SCHRITTMOTOR KONFIGURIEREN: DIV Einblenden */

$('#engine_conf').click(function () {
		$('#div_schrittmotor2').show("slow");
		$('#div_schrittmotor1').hide("slow");
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Ausstellung: einmal positiv drehen */
$('#button_schrittmotor1_1').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, 1, 0];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Ausstellung: einmal negativ drehen */
$('#button_schrittmotor1_2').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, -1, 0];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Maximalstellung: einmal positiv drehen */
$('#button_schrittmotor1_3').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, 1, 1];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Maximalstellung: einmal negativ drehen */
$('#button_schrittmotor1_4').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, -1, 1];
  ws.send(JSON.stringify(data));
});
/* Schrittmotor einmal positiv drehen*/
$('#engine1_up').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 0, 8, 0];
  ws.send(JSON.stringify(data));
});
/* Schrittmotor einmal negativ drehen*/
$('#engine1_down').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 0, -8, 0];
  ws.send(JSON.stringify(data));
});

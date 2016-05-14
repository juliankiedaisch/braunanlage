/* SCHRITTMOTOR KONFIGURIEREN: DIV Einblenden */
$('#engine_conf1').click(function () {
		$('#div_schrittmotor2').show("slow");
		$('#div_schrittmotor1').hide("slow");
});
/* SCHRITTMOTOR KONFIGURIEREN: DIV ausblenden */
$('#engine_conf2').click(function () {
		$('#div_schrittmotor1').show("slow");
		$('#div_schrittmotor2').hide("slow");
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Ausstellung: einmal positiv drehen */
$('#button_schrittmotor1_1').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, 1, 0];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine2: Ausstellung: einmal positiv drehen */
$('#button_schrittmotor2_1').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [1, 1, 1, 0];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Ausstellung: einmal negativ drehen */
$('#button_schrittmotor1_2').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, -1, 0];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine2: Ausstellung: einmal negativ drehen */
$('#button_schrittmotor2_2').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [1, 1, -1, 0];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Maximalstellung: einmal positiv drehen */
$('#button_schrittmotor1_3').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, 1, 1];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine2: Maximalstellung: einmal positiv drehen */
$('#button_schrittmotor2_3').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [1, 1, 1, 1];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Maximalstellung: einmal negativ drehen */
$('#button_schrittmotor1_4').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, -1, 1];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Maximalstellung: einmal negativ drehen */
$('#button_schrittmotor2_4').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [1, 1, -1, 1];
  ws.send(JSON.stringify(data));
});
/* Schrittmotor 1 einmal positiv drehen*/
$('#engine1_up').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 2, 1, 0];
  ws.send(JSON.stringify(data));
});
/* Schrittmotor 2 einmal positiv drehen*/
$('#engine2_up').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [1, 2, 1, 0];
  ws.send(JSON.stringify(data));
});11
/* Schrittmotor 1 einmal negativ drehen*/
$('#engine1_down').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 2, 0, 0];
  ws.send(JSON.stringify(data));
});
/* Schrittmotor 2 einmal negativ drehen*/
$('#engine2_down').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [1, 2, 0, 0];
  ws.send(JSON.stringify(data));
});

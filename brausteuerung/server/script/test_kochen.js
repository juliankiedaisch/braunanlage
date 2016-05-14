//KALIBRIEREN: DIV KALLIBRIEREN zeigen
$("#engine_kal1").click( function() {

  $('#div_schrittmotor3').show("slow");
  $('#div_schrittmotor1').hide("slow");

});
//KALIBRIEREN: DIV KALLIBRIEREN ausblenden/Kallibrieren beenden
$("#k_end").click( function() {

  $('#div_schrittmotor3').hide("slow");
  $('#div_schrittmotor1').show("slow");
});
//Informationen zum aktuellen Stand werden eingetragen
function input_kalibrieren(input) {
  $('#k_temp1').text(input[0] + "°C");
  $('#k_temp2').text(input[1] + "°C");
  $('#k_m_stellung').text(input[2] + "%");
  $('#k_status').text(input[3]);
}
//KALIBRIEREN: KALLIBRIEREN beginnen
$("#k_start").click( function() {
  data = [];
  data[0] = "kalibrieren";
  data[1] = 1;
  ws.send(JSON.stringify(data));
});

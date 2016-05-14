//LOG: ZEIGE ALLE Koch-LOGS
function make_log_liste_full(myOptions) {
//Selects werden gespeichert
  Selects2 = myOptions;
//Select wird ausgewaehlt
  mySelect = $('#select_koch_log_liste');
//Select wird geleert und
//das Feld "auswaehlen" wird hinzugefuegt
  mySelect.empty().append("<option value='' disabled selected hidden>ausw&auml;hlen</option>");
  $.each(myOptions, function(val, text) {
      mySelect.append($('<option></option>').val(text[0]).html(text[4] + ": " + text[2] + " (" + text[1] + ")"));
    });
}
$('#select_koch_log_liste').change(function () {
  var data = new Array();
  data[0] = "log_vorgang";
  data[1] = $(this).val();
  ws.send(JSON.stringify(data));
});

/* LOG: DIV LOG-Vorgang anzeigen/ausblenden */
$('#div_show_log').bind("DOMSubtreeModified",function(){
  if ($(this).is(':empty')) {
		$(this).css("display", "none");
	}
	else { $(this).css("display", "block");}
});
//LOG: Zeige Vorgang-Log
function show_log_vorgang(daten) {
  div = $("#div_show_log");
  //Div wird geleert
  div.empty();
  table = $('<table id=table_log align=center width=100%><tr></tr></table>');
  div.append(table);
  $("#table_log tr:last").after("<tr style='border-bottom:1px solid;'><td width=40%><b>Informationen</b></td><td><b>Motoren</b></td><td><b>Sensoren</b></td><td><b>Zeit</b></td></tr>");
  //div.append(table);
  //Div wird mit den Daten neu gefuellt
  $.each(daten, function (val, text) {
    style = "green";
    switch(parseInt(text[0])) {
      case 0,1:
        style = "green";
        break;
      case 2:
        style = "";
        break;
    }
    console.log(text[5]);
    zeit =
    $("#table_log tr:last").after("<tr style='color:"+style+";'><td>"+text[1]+"</td><td>"+text[2]+"</td><td>"+text[3]+"</td><td>"+text[5]+"</td></tr>");
  });



}

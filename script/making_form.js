var mySelect = $('#select_biertypen1');
var myOptions = ['Pils', 'Weizen', 'Brown Ale'];

/* Biertypen bearbeiten einblenden */
$('#button_biertyp1').click(function () {
		$('#div_biertyp2').show("slow");
		$('#div_biertyp1').hide("slow");
});

/* Biertypen bearbeiten ausblenden (Speichern) */
$('#button_biertyp2').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_biertyp2').hide("slow");
		myOptions.push($('#neu_biertyp_name').val());
		mySelect.append($('<option></option>').val($('#neu_biertyp_name').val()).html($('#neu_biertyp_name').val()));
    var data = new Array();
    data[0] = "beertyps";
    data[1] = myOptions;
    ws.send(JSON.stringify(data));
});
/*Biertyp bearbeiten ausblenden (Abbrechen) */
$('#button_biertyp3').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_biertyp2').hide("slow");

});

/* Option hinzufuegen */


$.each(myOptions, function(val, text) {
    mySelect.append(
        $('<option></option>').val(text).html(text)
    );
});

/* Schrittmotor */
$('#engine1_up').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, 512];
  alert(data);
  ws.send(JSON.stringify(data));
});
$('#engine1_down').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 0, 512];
  alert(data);
  ws.send(JSON.stringify(data));
});

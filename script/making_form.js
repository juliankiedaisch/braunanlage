var mySelect = $('#select_biertypen1');
var myOptions = ['Pils', 'Weizen', 'Brown Ale'];
var counter = 0;

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

/* Maischzeiten bearbeiten einblenden */
$('#button_maischzeit').click(function () {
		$('#div_maischzeit').show("slow");
		$('#div_biertyp1').hide("slow");
});

/*Maischzeiten bearbeiten ausblenden (Abbrechen) */
$('#button_maischzeit3').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_maischzeit').hide("slow");
		for (i= 0; i<counter; i++) {
			$('#div_inner_maischzeit ul').get(0).remove();
		}
		counter = 0;
});

/* Neue Maischzeit hinzufuegen */
$('#button_neu_maischzeit').click(function () {
		$('#div_inner_maischzeit').append('<ul class="actions"><li>'+ (counter + 1) + '. Phase:</li><li><input type="text" style="width:80px;" name="maischzeit_zeit[' + counter +']" id="maischzeit_zeit[' + counter +']" placeholder="min" /></li><li><input type="text" style="width:80px;" name="maischzeit_temp[' + counter +']" id="maischzeit_temp[' + counter +']" placeholder="°C" /></li></ul>');
		counter++;
});
/* Neue Maischzeit entfernen */
$('#button_weg_maischzeit').click(function () {
		if (counter >= 1) {
			counter--;
			$('#div_inner_maischzeit ul').get(counter).remove();
	}

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
  ws.send(JSON.stringify(data));
});
$('#engine1_down').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 0, 512];
  ws.send(JSON.stringify(data));
});

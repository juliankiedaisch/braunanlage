var mySelect = $('#select_biertypen1');
var myOptions = ['Pils', 'Weizen', 'Brown Ale'];
var counter = 0;
var NeuesRezept = [];
var Maischphasen = [];
var Hopfenbeigabe = [];
/* NEUES REZEPT: DIV Maischliste einblenden */
$('#liste_maischzeit').bind("DOMSubtreeModified",function(){
  if ($(this).is(':empty')) {
		$(this).css("display", "none");
	}
	else { $(this).css("display", "block");}
});
/* NEUES REZEPT: DIV Hopfenliste einblenden */
$('#liste_hopfen').bind("DOMSubtreeModified",function(){
  if ($(this).is(':empty')) {
		$(this).css("display", "none");
	}
	else { $(this).css("display", "block");}
});
/* NEUES REZEPT: Biertyp auswaehlen */
$('#select_biertypen1').change(function () {
		NeuesRezept[0] = $(this).val();
		$(this).css("background-color", "green")
						.css("color", "white")
						.css("opacity", "0.8");
});
/* NEUES REZEPT: Biername eingeben */
$('#biername').change(function () {
	if ($(this).val() != "") {
		NeuesRezept[1] = $(this).val();
		$(this).css("background-color", "green")
						.css("color", "white")
						.css("opacity", "0.8");
	} else { $(this).removeAttr('style'); }
});
/* NEUES REZEPT: Nachguss angeben*/
$('#nachguss').change(function () {
		if ($(this).val() != "") {
			NeuesRezept[3] = $(this).val();
			$(this).css("background-color", "green")
							.css("color", "white")
							.css("opacity", "0.8");
		} else { $(this).removeAttr('style');
	 		$(this).css("width", "80px");}
});
/* NEUES REZEPT: Kochzeit angeben*/
$('#kochzeit').change(function () {
		if ($(this).val() != "") {
			NeuesRezept[3] = $(this).val();
			$(this).css("background-color", "green")
							.css("color", "white")
							.css("opacity", "0.8");
		} else { $(this).removeAttr('style');
	 		$(this).css("width", "80px");}
});
/* NEUES REZEPT: Biertypen bearbeiten einblenden */
$('#button_biertyp1').click(function () {
		$('#div_biertyp2').show("slow");
		$('#div_biertyp1').hide("slow");
});
/* NEUES REZEPT: Biertypen bearbeiten ausblenden (Speichern) */
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
/*NEUES REZEPT: Biertyp bearbeiten ausblenden (Abbrechen) */
$('#button_biertyp3').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_biertyp2').hide("slow");

});
/*NEUES REZEPT:  Maischzeiten bearbeiten einblenden */
$('#button_maischzeit').click(function () {
		$('#div_maischzeit').show("slow");
		$('#div_biertyp1').hide("slow");
});
/*NEUES REZEPT:  Hopfenzeiten bearbeiten einblenden */
$('#button_hopfen').click(function () {
		$('#div_hopfen').show("slow");
		$('#div_biertyp1').hide("slow");
});
/*NEUES REZEPT:  Maischzeiten Speichern */
$('#button_maischzeit2').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_maischzeit').hide("slow");
		$('#liste_maischzeit').empty();
		var a = 0;
		var maisch_html = "";
		/* Alle Inputs werden abgefragt. Da pro Maischzeit immer 2 inputs existieren muss hier der Counter verdopplet werden. */
		for (i= 0; i<(counter*2); i++) {
			/* Counter beginnt bei 0, und bei allen geraden inputs ist die Zeit gegeben. bei den ungeraden deshalb die Temperatur */
			if(i%2==0) {
				/* Zeit */
				Maischphasen[a] = [$('#div_inner_maischzeit input').get(i).value];
				maisch_html = $('#div_inner_maischzeit input').get(i).value;
			}
			else {
				/* Temperatur */
				Maischphasen[a].push($('#div_inner_maischzeit input').get(i).value);
				$('#liste_maischzeit').append('<ul class="actions"><li>' + (a +1) + '. Phase: ' + maisch_html + ' Minuten bei ' + $('#div_inner_maischzeit input').get(i).value + '°C');
				maisch_html = "";
				a++;
			}
		}
		NeuesRezept[2] = Maischphasen;
		var data = new Array();
		data[0] = "beertyps";
    data[1] = NeuesRezept;
    ws.send(JSON.stringify(data));
});
/*NEUES REZEPT:  Hopfenzugabe Speichern */
$('#button_hopfen2').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_hopfen').hide("slow");
		$('#liste_hopfen').empty();
		var a = 0;
		var hopfen_html = "";
		/* Alle Inputs werden abgefragt. Da pro Hopfenzugabe immer 2 inputs existieren muss hier der Counter verdopplet werden. */
		for (i= 0; i<(counter*2); i++) {
			/* Counter beginnt bei 0, und bei allen geraden inputs ist die Zeit gegeben. bei den ungeraden deshalb der Name des Hopfens */
			if(i%2==0) {
				/* Zeit */
				Hopfenbeigabe[a] = [$('#div_inner_hopfen input').get(i).value];
				hopfen_html = $('#div_inner_hopfen input').get(i).value;
			}
			else {
				/* Temperatur */
				Hopfenbeigabe[a].push($('#div_inner_hopfen input').get(i).value);
				$('#liste_hopfen').append('<ul class="actions"><li>' + (a +1) + '. Hopfengabe: Nach ' + hopfen_html + ' Minuten (' + $('#div_inner_hopfen input').get(i).value + ')');
				hopfen_html = "";
				a++;
			}
		}
		NeuesRezept[5] = Hopfenbeigabe;
		var data = new Array();
		data[0] = "beertyps";
    data[1] = NeuesRezept;
    ws.send(JSON.stringify(data));
});
/*NEUES REZEPT: Maischzeiten bearbeiten ausblenden (Abbrechen) */
$('#button_maischzeit3').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_maischzeit').hide("slow");
});
/*NEUES REZEPT: Hopfen bearbeiten ausblenden (Abbrechen) */
$('#button_maischzeit3').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_hopfen').hide("slow");
});
/*NEUES REZEPT:  Neue Maischzeit hinzufuegen */
$('#button_neu_maischzeit').click(function () {
		$('#div_inner_maischzeit').append('<ul class="actions"><li>'+ (counter + 1) + '. Phase:</li><li><input type="number" min=0 max=400 style="width:80px;" name="maischzeit_zeit[' + counter +']" id="maischzeit_zeit[' + counter +']" placeholder="min" /></li><li><input type="number" min=20 max=100 style="width:80px;" name="maischzeit_temp[' + counter +']" id="maischzeit_temp[' + counter +']" placeholder="°C" /></li></ul>');
		counter++;
});
/*NEUES REZEPT:  Neue Hopfenbeigabe hinzufuegen */
$('#button_neu_hopfen').click(function () {
		$('#div_inner_hopfen').append('<ul class="actions"><li>'+ (counter + 1) + '. Hopfengabe:</li><li><input type="number" min=0 max=400 style="width:80px;" name="hopfen_zeit[' + counter +']" id="hopfen_zeit[' + counter +']" placeholder="min" /></li><li><input type="text" style="width:120px;" name="hopfen_name[' + counter +']" id="hopfen_name[' + counter +']" placeholder="Name" /></li></ul>');
		counter++;
});
/*NEUES REZEPT:  Neue Maischzeit entfernen */
$('#button_weg_maischzeit').click(function () {
		if (counter >= 1) {
			counter--;
			$('#div_inner_maischzeit ul').get(counter).remove();
	}
});
/*NEUES REZEPT:  Neue Hopfenzugabe entfernen */
$('#button_weg_hopfen').click(function () {
		if (counter >= 1) {
			counter--;
			$('#div_inner_hopfen ul').get(counter).remove();
	}
});
/*NEUES REZEPT:  Option für Biertyp hinzufuegen */
$.each(myOptions, function(val, text) {
    mySelect.append(
        $('<option></option>').val(text).html(text)
    );
});
/* SCHRITTMOTOR KONFIGURIEREN: DIV Einblenden */

$('#engine_conf').click(function () {
		$('#div_schrittmotor2').show("slow");
		$('#div_schrittmotor1').hide("slow");
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Ausstellung: einmal positiv drehen */
$('#button_schrittmotor1_1').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, 1];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: AUsstellung: einmal negativ drehen */
$('#button_schrittmotor1_2').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 0, 1];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Maximalstellung: einmal positiv drehen */
$('#button_schrittmotor1_3').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, 1];
  ws.send(JSON.stringify(data));
});
/* SCHRITTMOTOR KONFIGURIEREN: Engine1: Maximalstellung: einmal negativ drehen */
$('#button_schrittmotor1_4').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 0, 1];
  ws.send(JSON.stringify(data));
});
/* Schrittmotor einmal positiv drehen*/
$('#engine1_up').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 1, 512];
  ws.send(JSON.stringify(data));
});
/* Schrittmotor einmal negativ drehen*/
$('#engine1_down').click(function () {
  var data = new Array();
  data[0] = "engine";
  data[1] = [0, 0, 256];
  ws.send(JSON.stringify(data));
});

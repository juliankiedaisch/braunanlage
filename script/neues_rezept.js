
var counter = 0;
var Rezept = [];
var Maischphasen = [];
var Hopfenbeigabe = [];

function make_maischphasen(type, myOptions) {
//Neuer Eintrag(auch mehrere) oder ein Eintrag loeschen
  switch(type) {
    //Eintrag wird geloescht
    case 0:
      if(Maischphasen.length>0) {
        $('#div_inner_maischzeit ul').get((Maischphasen.length-1)).remove();
        $('#liste_maischzeit ul').get((Maischphasen.length-1)).remove();
        Maischphasen.pop();
      }
      break;
    //Neuer Eintrag
    case 1:
    //Maischphasen wird ueberschrieben
      Maischphasen = myOptions;
      //Liste im ALlgemeinteil wird geloescht
      $('#liste_maischzeit').empty();
      //Liste in der Bearbeitungsmaske wird geloescht
      $('#div_inner_maischzeit').empty();
      for (i=0; i<myOptions.length; i++) {
        console.log(myOptions);
        //Liste im Allgemeinteil wird neu erstellt:
        $('#liste_maischzeit').append('<ul class="actions"><li>' + (i +1) + '. Phase: ' + myOptions[i][0] + ' Minuten bei ' + myOptions[i][1] + '°C');
        //Liste in der Bearbeitungsmaske wird neu erstellt
        $('#div_inner_maischzeit').append('<ul class="actions"><li><input type="number" min=0 max=400 style="width:80px;" placeholder="min" value="'+ myOptions[i][0] + '" /></li><li><input type="number" min=20 max=100 style="width:80px;" placeholder="°C" value="'+ myOptions[i][1] + '" /></li></ul>');
      }
      break;
  }
}

function make_selects(myOptions) {
  mySelect = [];
  mySelect[0] = $('#select_biertypen1');
  mySelect[1] = $('#select_biertypen2');
  mySelect[0].empty().append("<option value='' disabled selected hidden>ausw&auml;hlen</option>");
  mySelect[1].empty().append("<option value='' disabled selected hidden>ausw&auml;hlen</option>");
  a=0
  $.each(myOptions, function(val, text) {
    for (x=0; x<2; x++) {
      mySelect[x].append(
          $('<option></option>').val(text[0]).html(text[1])
      );
    }
    a++;
  });
}

/* NEUES REZEPT: DIV Rezepteingabe einblenden */
$('#neues_rezept1').click(function (){
  $('#div_neues_rezept2').show("slow");
  $('#div_neues_rezept1').hide("slow");
});
/* NEUES REZEPT: DIV Rezepteingabe ausblenden */
$('#neues_rezept2').click(function (){
  $('#div_neues_rezept1').show("slow");
  $('#div_neues_rezept2').hide("slow");
});
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
    $("#test_span").text($(this).val());
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
/* NEUES REZEPT: Neuer Biertyp Speichern */
$('#button_biertyp2').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_biertyp2').hide("slow");
    var data = new Array();
    var data2 = new Array();
    data[0] = "b_biertyp";
    data2[0] = 1;
    data2[1] = $("#neu_biertyp_name").val();
    data[1] = data2;
    ws.send(JSON.stringify(data));
});
/* NEUES REZEPT:Biertyp Loeschen */
$('#button_biertyp4').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_biertyp2').hide("slow");
    var data = new Array();
    var data2 = new Array();
    data[0] = "b_biertyp";
    data2[0] = 0;
    data2[1] = $("#select_biertypen2").val();
    data[1] = data2;
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
		var a = 0;
    var phasen = []
		/* Alle Inputs werden abgefragt. Da pro Maischzeit immer 2 inputs existieren muss hier der Counter verdopplet werden. */
		for (i= 0; i<(Maischphasen.length*2); i++) {
			/* Counter beginnt bei 0, und bei allen geraden inputs ist die Zeit gegeben. bei den ungeraden deshalb die Temperatur */
			if(i%2==0) {
				/* Zeit */
				phasen[a] = [$('#div_inner_maischzeit input').get(i).value];
			}
			else {
				/* Temperatur */
				phasen[a].push($('#div_inner_maischzeit input').get(i).value);
				a++;
			}
		}
    make_maischphasen(1, phasen);
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
		Rezept[5] = Hopfenbeigabe;
		var data = new Array();
		data[0] = "beertyps";
    data[1] = Rezept;
    ws.send(JSON.stringify(data));
});
/*NEUES REZEPT: Maischzeiten bearbeiten ausblenden (Abbrechen) */
$('#button_maischzeit3').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_maischzeit').hide("slow");
});
/*NEUES REZEPT: Hopfen bearbeiten ausblenden (Abbrechen) */
$('#button_hopfen3').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_hopfen').hide("slow");
});
/*NEUES REZEPT:  Neue Maischzeit hinzufuegen */
$('#button_neu_maischzeit').click(function () {
    phasen = Maischphasen;
    phasen.push(["",""]);
		make_maischphasen(1, phasen);
});
/*NEUES REZEPT:  Neue Hopfenbeigabe hinzufuegen */
$('#button_neu_hopfen').click(function () {
		$('#div_inner_hopfen').append('<ul class="actions"><li>'+ (counter + 1) + '. Hopfengabe:</li><li><input type="number" min=0 max=400 style="width:80px;" name="hopfen_zeit[' + counter +']" id="hopfen_zeit[' + counter +']" placeholder="min" /></li><li><input type="text" style="width:120px;" name="hopfen_name[' + counter +']" id="hopfen_name[' + counter +']" placeholder="Name" /></li></ul>');
		counter++;
});
/*NEUES REZEPT:  Neue Maischzeit entfernen */
$('#button_weg_maischzeit').click(function () {
    make_maischphasen(0, Maischphasen);
});
/*NEUES REZEPT:  Neue Hopfenzugabe entfernen */
$('#button_weg_hopfen').click(function () {
		if (counter >= 1) {
			counter--;
			$('#div_inner_hopfen ul').get(counter).remove();
	}
});

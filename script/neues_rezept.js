
var Rezept = {rezept_id : null,
 							maischphasen : null,
							hopfenbeigabe : null,
							biertyp : null,
							biername : null,
							kochzeit : null,
							nachguss : null,
							};
var Maischphasen = [];
var Hopfenbeigabe = [];
//Eingabemaske wird befuellt
function rezept_einlesen(rezept) {
  //Biertyp
  $("#select_biertypen1 option[value='" + rezept.biertyp + "']").attr('selected', true);
  //Biername
  $("#biername").val(rezept.biername);
  //Maischphasen
  make_maischphasen(1, rezept.maischphasen);
  //Hopfenbeigabe
  make_hopfenphasen(1, rezept.hopfenbeigabe);
  //Kochzeit
  $("#kochzeit").val(rezept.kochzeit);
  //Nachguss
  $("#nachguss").val(rezept.nachguss);
  //Rezept_ID
  $("#Rezept_id").val(rezept.rezept_id);
}
//Loescht alle EIntraege im Object Rezept
function delete_rezept_obj(obj) {
	delete obj.rezept_id;
	delete obj.maischphasen;
	delete obj.hopfenbeigabe;
	delete obj.biertyp;
	delete obj.biername;
	delete obj.kochzeit;
	delete obj.nachguss;
}
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
function make_hopfenphasen(type, myOptions) {
//Neuer Eintrag(auch mehrere) oder ein Eintrag loeschen
  switch(type) {
    //Eintrag wird geloescht
    case 0:
      if(Hopfenbeigabe.length>0) {
        $('#div_inner_hopfen ul').get((Hopfenbeigabe.length-1)).remove();
        $('#liste_hopfen ul').get((Hopfenbeigabe.length-1)).remove();
        Hopfenbeigabe.pop();
      }
      break;
    //Neuer Eintrag
    case 1:
    //Maischphasen wird ueberschrieben
      Hopfenbeigabe = myOptions;
      //Liste im ALlgemeinteil wird geloescht
      $('#liste_hopfen').empty();
      //Liste in der Bearbeitungsmaske wird geloescht
      $('#div_inner_hopfen').empty();
      for (i=0; i<myOptions.length; i++) {
        console.log(myOptions);
        //Liste im Allgemeinteil wird neu erstellt:
        $('#liste_hopfen').append('<ul class="actions"><li>' + (i +1) + '. Hopfengabe: Nach ' + myOptions[i][0] + ' Minuten (' + myOptions[i][1] + ')');
        //Liste in der Bearbeitungsmaske wird neu erstellt
        $('#div_inner_hopfen').append('<ul class="actions"><li>'+ (i + 1) + '. Hopfengabe:</li><li><input type="number" min=0 max=400 style="width:80px;" placeholder="min" value="' + myOptions[i][0] + '" /></li><li><input type="text" style="width:120px;" placeholder="Name" value="' + myOptions[i][1] + '" /></li></ul>');
      }
      break;
  }
}
//NEUES REZEPT: BIERTYPEN Selects
function make_selects(myOptions) {
  mySelect = [];
  mySelect[0] = $('#select_biertypen1');
  mySelect[1] = $('#select_biertypen2');
  mySelect[0].empty().append("<option value='' disabled selected hidden>ausw&auml;hlen</option>");
  mySelect[1].empty().append("<option value='' disabled selected hidden>ausw&auml;hlen</option>");
  $.each(myOptions, function(val, text) {
    for (x=0; x<2; x++) {
      mySelect[x].append(
          $('<option></option>').val(text[0]).html(text[1])
      );
    }
  });
}
//NEUES REZEPT: ZEIGE ALLE REZEPTE
function select_rezepte(myOptions) {
  mySelect = $('#select_alle_rezepte');
  mySelect.empty();
  $.each(myOptions, function(val, text) {
      mySelect.append($('<option></option>').val(text[0]).html(text[1] + "(" + text[2] + ")"));
    });
}
/*NEUES REZEPT:  REZEPT Speichern */
$('#rezept_speichern').click(function () {
	//Erstmal checken, ob alle Informationen da sind.
  //Biertyp
  biertyp = $('#select_biertypen1').val();
  //Biername
  biername = $("#biername").val();
  //Maischphasen
  maischphasen = Maischphasen;
  //Hopfenbeigabe
  hopfenbeigabe = Hopfenbeigabe;
  //Kochzeit
  kochzeit = $("#kochzeit").val();
  //Nachguss
  nachguss = $("#nachguss").val();
  //Rezept_ID
  rezept_id = $("#rezept_id").val();
  //Rezept Object wird geleert
  delete_rezept_obj(Rezept);

  if (biertyp && biername && maischphasen.length>0 && hopfenbeigabe.length>0 && kochzeit && nachguss) {

    Rezept.rezept_id = rezept_id;
    Rezept.maischphasen = maischphasen;
    Rezept.hopfenbeigabe = hopfenbeigabe;
    Rezept.biertyp = biertyp;
    Rezept.biername = biername;
    Rezept.kochzeit = kochzeit;
    Rezept.nachguss = nachguss;
    data = [];
    data[0] = "rezept";
    data[1] = Rezept;
    ws.send(JSON.stringify(data));
    message = {};
    message.ctype = 1;
    message.cstatus = 0;
    message.cnote = "Rezept wurde gespeichert"
    show_noty(message);
  } else {
    message = {};
    message.ctype = 2;
    message.cstatus = 0;
    message.cnote = "Es fehlen noch Eintr&auml;ge! Rezept konnte nicht gespeichert werden."
    show_noty(message);
  }


});
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
    var a = 0;
    var phasen = []
		/* Alle Inputs werden abgefragt. Da pro Hopfengabe immer 2 inputs existieren muss hier der Counter verdopplet werden. */
		for (i= 0; i<(Hopfenbeigabe.length*2); i++) {
			/* Counter beginnt bei 0, und bei allen geraden inputs ist der Hopfenname gegeben. bei den ungeraden deshalb die Temperatur */
			if(i%2==0) {
				/* Zeit */
				phasen[a] = [$('#div_inner_hopfen input').get(i).value];
			}
			else {
				/* Name des Hopfens */
				phasen[a].push($('#div_inner_hopfen input').get(i).value);
				a++;
			}
		}
    make_hopfenphasen(1, phasen);
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
  phasen = Hopfenbeigabe;
  phasen.push(["",""]);
  make_hopfenphasen(1, phasen);
});
/*NEUES REZEPT:  Neue Maischzeit entfernen */
$('#button_weg_maischzeit').click(function () {
    make_maischphasen(0, Maischphasen);
});
/*NEUES REZEPT:  Neue Hopfenzugabe entfernen */
$('#button_weg_hopfen').click(function () {
	  make_hopfenphasen(0, Hopfenbeigabe);
});
/*NEUES REZEPT:  Speichernbutton in Aendernbutton aendern */
$('#rezept_id').change(function () {
  //Wenn eine ID in das Feld eingefuegt wird, aendert sich der Button in "Rezept Aendern"
	  if($.isNumeric(this.val())) {
      $("#rezept_speichern").html = "Rezept &auml;ndern"
      $("#rezept_ueberschrift").html = "Rezept &Auml;ndern"
    } else {
      $("#rezept_speichern").html = "Rezept speichern"
      $("#rezept_ueberschrift").html = "Neues Rezept"
    }
});

var mySelect = $('#select_biertypen1');
var myOptions = {
    1 : 'Pils',
    2 : 'Weizen',
		3 : 'Brown Ale'
};

/* Biertypen bearbeiten einblenden */
$('#button_biertyp1').click(function () {
		$('#div_biertyp2').show("slow");
		$('#div_biertyp1').hide("slow");
});

/* Biertypen bearbeiten ausblenden (Speichern) */
$('#button_biertyp2').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_biertyp2').hide("slow");
		a = Object.keys(myOptions).length + 1;
		$('#biertyp_message').text(a);
		myOptions.a = $('#neu_biertyp_name').val();
		mySelect.append($('<option></option>').val(a).html($('#neu_biertyp_name').val()));
		ws.send(JSON.stringify(myOptions));
});
/*Biertyp bearbeiten ausblenden (Abbrechen) */
$('#button_biertyp3').click(function () {
		$('#div_biertyp1').show("slow");
		$('#div_biertyp2').hide("slow");

});

/* Option hinzufuegen */


$.each(myOptions, function(val, text) {
    mySelect.append(
        $('<option></option>').val(val).html(text)
    );
});

$('#select_biertypen1').change(function () {
		$('#biertyp_message').text($('#select_biertypen1 option:selected').val());
});

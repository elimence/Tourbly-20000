
function init() {
	
    var destination_tag = document.getElementById('destination');
	var options = {
	componentRestrictions: {country: 'au'}
	};
	var place;
	var autocomplete = new google.maps.places.Autocomplete(destination_tag, options);
	
	var previous_place = document.getElementById("destination").value;
	google.maps.event.addListener(autocomplete, 'place_changed', function() {
        place = autocomplete.getPlace();
        var current_place = document.getElementById("languages").value;;
        if (previous_place != current_place) {
        	document.getElementById("filter-form").submit();
        }
    });
}
	






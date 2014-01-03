function attachFilterButtonListener() {
	var search_form = document.getElementById("filter-form");
}

function filterButtonClickListener (evt) {
	var arrivalText = $('#arrival').val(),
		departureText = $('#departure').val();

	if (arrivalText == '' || departureText == '') {
		alert('Please provide your arrival & departure dates');
		evt.preventDefault(); return;
	}

	var arrival = new Date(new Date(arrivalText).setHours(new Date().getHours() + 5)),
	    departure = new Date(departureText),
	    today = new Date();
	
	if (arrival < today) {
		alert('Sorry. Your arrival date cannot be a past date.');
		evt.preventDefault(); return;
	} else if (departure < arrival) {
		alert('Your departure date must be after your arrival date.');
		evt.preventDefault(); return;
	}
}

function searchSelectedListeners() {
	var search_form = document.getElementById("filter-form");

    $(document).ready(function(){
       var clicknum = 0;
       var previous_content = document.getElementById("gender").value;
       $("#gender").click(function(){
        clicknum++;
        if(clicknum == 1){
          var current_content = document.getElementById('gender').value;
          if (current_content != previous_content) {
            search_form.submit();
          }
          clicknum = 0;
        }
       });
      });

    $(document).ready(function(){
       var clicknum = 0;
       var previous_content = document.getElementById("languages").value;
       $("#languages").click(function(){
        clicknum++;
        if(clicknum == 1){
          var current_content = document.getElementById('languages').value;
          if (current_content != previous_content) {
            search_form.submit();
          }
          clicknum = 0;
        }
       });
      });

    $(document).ready(function(){
       var clicknum = 0;
       var previous_content = document.getElementById("arrival").value;
       $("#arrival").click(function(){
        clicknum++;
        if(clicknum == 1){
          var current_content = document.getElementById('arrival').value;
          $("#arrival").click(function() {
            console.log(current_content)
            if (current_content != previous_content) {
              search_form.submit();
            }
          });
          clicknum = 0;
        }
       });
      });

    $(document).ready(function(){
       var clicknum = 0;
       var previous_content = document.getElementById("select-beast").value;
       $("#destination").click(function(){
        clicknum++;
        console.log(previous_content);
        if(clicknum == 1){
          var current_content = document.getElementById('select-beast').value;
          if (current_content != previous_content) {
            search_form.submit();
          }
          clicknum = 0;
        }
       });
      });

    $(document).ready(function() {
      $("#select-beast").click(function() {
        console.log("option clicked");
      });
    });
}
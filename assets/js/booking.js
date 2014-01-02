function attachPayButtonListener() {
  $('#pay-button').on('click', payButtonClickListener);
}

function payButtonClickListener (evt) {
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
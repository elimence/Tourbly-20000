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

function dayAndChargeManipulations() {
  changeTourDays();
  changeTourCharge();
}

function getTourDays() {
  var arrival_date = document.getElementById("arrival").value;
  var departure_date = document.getElementById("departure").value;

  arrival_date = Date.parse(arrival_date);
  departure_date = Date.parse(departure_date);

  if (arrival_date && departure_date) {
    var tour_days = new TimeSpan(departure_date - arrival_date);
    return tour_days.days;
  }
  return 0;
}

function changeTourDays() {
  var tour_days = getTourDays();

  document.getElementById("tour_days").innerHTML = tour_days;
}

function changeTourCharge() {
  var tour_days = getTourDays();
  var charge = tour_days * 50
  document.getElementById("tour_charge").innerHTML = "$ " + charge + ".00"
}

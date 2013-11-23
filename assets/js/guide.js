function handleMandrillResponse(res) {
	if (!res[0].reject_reason) {
		// was good
		$('#bookModal').modal('hide');
		$('#bookGuide').attr('disabled', 'disabled');
		console.log($('#bookGuide').html('Booking Request Sent'));
	} else {
		console.log('Error sending mail');
	}
}

function authLoginHandler() {
	var url = location.href.replace(/guides\/.+/, 'signin');
	location.href = url;
}

function authSignupHandler() {
	var url = location.href.replace(/guides\/.+/, 'signup');
	location.href = url;
}

function doBookingHandler () {
	if ($('#user-email').val()) {
		$('#bookModal').modal('show');
	} else {
		$('#authModal').modal('show');
		// var signinUrl = location.href.replace(/guides\/.+/, 'signin');
		// alert('You must sign up to complete your booking');
		// location.href = signinUrl;
	}
}

function bookingHandler () {
	var m = new mandrill.Mandrill('H6IKRz-zlEYqQuX2njpRMA');

	// create a variable for the API call parameters
	var params = {
	    "message": {
	        "from_email":"tourblyinfo@gmail.com",
	        "to":[{"email":"precious@meltwater.org"}],
	        "subject": "Testing the Mandrill API",
	        "autotext": true,
	        "track_opens": true,
	        "track_clicks": true,
	        "html": "<h1>Booking Confirmation</h1><p>Hello Precious. You recently booked Nana Kay to be your tour guide on you trip to Accra, Ghana.<br />Here is his contact information so you can get in touch:<br /><br />Telephone: +233244792042<br />Email: nanakay@google.com<br /><strong>Address</strong><br />21 Naa Adzetsoo Nkrumah Street<br />Teshie, Accra<br />Ghana</p>"
	    }
	};

	function sendTheMail() {
	    m.messages.send(params, function(res) {
	        handleMandrillResponse(res);
	    }, function(err) {
	        handleMandrillResponse(err);
	    });
	}

	sendTheMail();
}
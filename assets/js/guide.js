function init() {
	$('.ago').each(function (index, item) {
		// Grag the raw date (specified in the format: YYYY-MM-DD HH:mm:ss) 
		// and swap the text out with the timeago equivalent
		$(item).html(moment($(item).html(), "YYYY-MM-DD HH:mm:ss").fromNow());
	});
  attachSubmitReviewListener();
  attachBookGuideClickListener();
}

function attachBookGuideClickListener() {
  $('#bookGuide').on('click', bookGuideClickListener);
}

function bookGuideClickListener(e) {
  var cookies = $.cookie();
  if (!(cookies.query && cookies.authenticator)) {
    e.preventDefault();
    // alert(location.href + '/book');
    // Set the redirect cookie here...
    $.cookie('redirects', location.href + '/book', { expires: 7, path: '/' });
    $('#authRequired').modal();
  }
}

function attachSubmitReviewListener() {
  if ($('#submit-btn').length) {
    $('#submit-btn').on('click', submitReviewClickListener);
  }
}

function submitReviewClickListener(e) {
  var nameInputPresent = $('#name').length;
  var rating = $('#rating').val(),
      comment = $('#comment').val();
  if (nameInputPresent) {
    var name   = $('#name').val();
    if (!(name && rating && comment)) {
      e.preventDefault();
      alert('All fields are required to save your review');
    }
  } else {
    if (!(rating && comment)) {
      e.preventDefault();
      alert('All fields are required to save your review');
    }
  }
}
function init() {
	$('.ago').each(function (index, item) {
		// Grag the raw date (specified in the format: YYYY-MM-DD HH:mm:ss) 
		// and swap the text out with the timeago equivalent
		$(item).html(moment($(item).html(), "YYYY-MM-DD HH:mm:ss").fromNow());
	});
  attachSubmitReviewListener();
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
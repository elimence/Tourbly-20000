function init() {
	$('.ago').each(function (index, item) {
		// Grag the raw date (specified in the format: YYYY-MM-DD HH:mm:ss) 
		// and swap the text out with the timeago equivalent
		$(item).html(moment($(item).html(), "YYYY-MM-DD HH:mm:ss").fromNow());
	});
}
'use strict'

function TourblyCtrl($scope, $window, $http) {
	$scope.apiBase   = '/oauth';
	$scope.revokeUrl = 'https://accounts.google.com/o/oauth2/revoke?token';

	$scope.uDat = {email: "", verified: ""};

	$scope.userData = {
		email      : "",
		gender     : "",
		picture    : "",
		last_name  : "",
		languages  : "",
		activated  : "",
		first_name : "",
		redirects  : ""
	};


	$scope.accessToken = {
		get: function()       {
			var cookies = document.cookie.split(';');
			for (var i=0; i<cookies.length; i++) {
				var cookie = cookies[i].trim();
				if (cookie.indexOf('access_token')  == 0)
					return cookie.substring('access_token'.length, cookie.length);
			}
			return null;
		},
		del: function()       { document.cookie='access_token=';
		},
		save: function(token) { document.cookie='access_token='+token;
		}
	};


	$scope.signin = function(authResult) {
		gapi.client.load('oauth2', 'v2', function() {
			if (authResult['access_token']) {
				gapi.client.oauth2.userinfo.get().execute(function(resp) {
					//save token
					$scope.accessToken.save(authResult['access_token']);
					$scope.userData.email     = resp.email;
					$scope.userData.activated = resp.verified_email;
				});

			} else if (authResult['error']) {
				console.log('There was an error: ' + authResult['error']);
			}
		});


		gapi.client.load('plus', 'v1', function() {
			if (authResult['access_token']) {
				gapi.client.plus.people.get( {'userId' : 'me'} ).execute(function(resp) {
					// console.log(resp);
					$scope.userData.gender     = resp.gender;
					$scope.userData.picture    = resp.image.url;
					$scope.userData.languages  = resp.language;
					$scope.userData.last_name  = resp.name.familyName;
					$scope.userData.first_name = resp.name.givenName;

					// console.log($scope.userData);
					var redirects_cookie = $.cookie('redirects');
					if (redirects_cookie != 'undefined') {
						$scope.userData.redirects = redirects_cookie;
					}

					$scope.outBound.post({
						async : "false",
						url   : $scope.apiBase,
						dat   : $scope.userData
					}).done(function(data) {
						document.cookie=data.split("*-*")[0];
						document.cookie=data.split("*-*")[1];
						if (data.split("*-*")[2].length > 1) {
							location.replace(data.split("*-*")[2]);
						} else {
							location.reload();
						}
					});

				});

			} else if (authResult['error']) {
				console.log('There was an error: ' + authResult['error']);
			}
		});
	};// end function signup

	$scope.disconnect = function(access_token) {
		$('#confirmDisconnect').modal();
	}// end function disconnect

	$scope.revoke = function(tasks) {
		$.ajax({
			type: 'GET',
		    url: $scope.revokeUrl + $scope.accessToken.get(),
		    async: false,
		    contentType: "application/json",
		    dataType: 'jsonp',
		    success: function(nullResponse) {
		    	console.log("Successfully disconnected!");
		    	tasks();

		    	$scope.accessToken.del();
		    	$window.alert("Disconnect Successfull");
		    	$window.location.replace('/logout');
		    },
		    error: function(e) {
		    	console.log("Failed to disconnect! : ", e);
		    	alert("Failed to disconnect! Please go to https://plus.google.com/apps to disconnect manually")
		      // Handle the error
		      // console.log(e);
		      // You could point users to manually disconnect if unsuccessful
		      // https://plus.google.com/apps
		    }
		});
	};

	$scope.conDisconnect = function() {
		if (!($('#newpass').val())) { // If no password was entered
		  var proceed = confirm("If you do not type a password, your Tourbly account will be closed! Are you sure you want to continue?");
		  if (proceed) {
		    // You can disconnect from google and close the account
		    $('#confirmDisconnect').modal('hide');
		    $scope.revoke(function() {
		    	$scope.outBound.post({
		    		async : "false",
		    		url   : '/disconnect',
		    	}).done(function(data) {
		    		// console.log('Successfully deleted tourist', data);
		    	});
		    });
		  } else {
		    // Do nothing
		  }
		} else {
		  var pass = $('#newpass').val(),
		      confirmPass = $('#confirm').val();

		  if (!confirmPass) {
		    alert('Please confirm you password');
		  } else if (pass != confirmPass) {
		    alert('Your passwords do not match');
		  } else {
		  	if (pass.length<6)
		  		alert("You password must be 6 characters or more");
		  	else {
		  		$('#confirmDisconnect').modal('hide');
		  		$http.post('/switchaccount', pass)
		  		.success(function(res){
		  			$scope.revoke(function() {
		  				alert("You will now be logged out, please login with new password");
		  				window.location.replace('/logout');
		  			})
		  		});
		  	}
		  }
		}
	}

	$scope.outBound =  {
		get: function(_args) {
			return $.ajax({
				type        : 'GET',
				url         : $scope.apiBase,
				async       : _args.async,
				contentType : 'application/json',
				dataType    : 'jsonp'
			})
			.always(function() {
				console.log("ALWAYS FUNCTION CALLED - GET");
			})
			.fail(function(data) {
				console.log("FAILURE, GET TO SERVER WITH STATUS: ");
				console.log(data);
			});
		},
		post: function(_args) {
			return $.ajax({
				type        : 'POST',
				url         : _args.url,
				async       : _args.async,
				data        : _args.dat
			})
			.fail(function(err) {
				console.log("FAILURE, POST TO SERVER WITH STATUS: ");
				console.log(err);
			});
		}
	}// end object outBound

	$window.renderSignin = function() {
		if ($('#signup-form').is(':visible')) {
			gapi.signin.render('customBtn', {
				'callback': $scope.signin,
				'immedediate': false,
				'clientid': '1066634592899-vq0boe9dv5s49lf3jghr6qo825bvesg9.apps.googleusercontent.com',
				'cookiepolicy': 'single_host_origin',
				'requestvisibleactions': 'http://schemas.google.com/AddActivity',
				'scope': 'https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email'
			});
		}

		if ($('#mobile').is(':visible')) {
			gapi.signin.render('customBtn_M', {
				'callback': $scope.signin,
				'immedediate': false,
				'clientid': '1066634592899-vq0boe9dv5s49lf3jghr6qo825bvesg9.apps.googleusercontent.com',
				'cookiepolicy': 'single_host_origin',
				'requestvisibleactions': 'http://schemas.google.com/AddActivity',
				'scope': 'https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email'
			});
		}
	}// end function renderSignin
}// end controller TourblyCtrl


function PaymentCtrl($scope, $window, $http) {

	$scope.price = "0.00";
	$scope.duration = '0';

	$scope.getParams = function() {
        return {
            end:$scope.endModel,
            start:$scope.startModel,
            price:$scope.price,
            guideID:$scope.guideID,
            message:$scope.guideMessage,
            touristID:$scope.touristID,
            description:$scope.duration + " - day guided tour to "+ document.getElementById('placeName').value,
            paymentStatus:"Completed"
        };
    };

	$scope.success = function(status) {
		$window.console.log('Purchase Completed Successfully : ', status);
		$('#bookingForm').submit();
	};// end function success

	$scope.failure = function(status) {
		$window.console.log('Purchase Failed : ', status);
	};// end function failure

	$scope.purchase = function() {

		if ($scope.startModel == undefined) {
			alert("Please tell us when your tour starts");
		} else if ($scope.endModel == undefined) {
			alert("Please tell us when your tour will end");
		} else {

			var today         = new Date();
			// add 10 hours to selected dat to allow users to specify one day tours
			var departureDate = new Date(new Date($scope.endModel).setHours(new Date().getHours() + 10));
			// add 5 hours to allow users to specify today as tour start date
			var arrivalDate   = new Date(new Date($scope.startModel).setHours(new Date().getHours() + 5));

			if (arrivalDate < today) {
				alert('Sorry. Your tour start date cannot be a past date.');
			} else if (departureDate < arrivalDate) {
				alert('Your tour end date must be after your arrival date.');
			} else {

				// $http({method: 'GET', url: '/payments/'+ $scope.duration})
				// 	.success(function(data, status, headers, config) {
				// 		console.log('success with : ', data);

				// 		$scope.progress.stop();
				// 		goog.payments.inapp.buy({
				// 			'jwt'     : data,
				// 			'success' : $scope.success,
				// 			'failure' : $scope.failure
				// 		});
				// 	})
				// 	.error(function(data, status, headers, config) {
				// 		console.log('error');
				// 	})
				// ; // end http invocation

				$http({url: '/payments/'+ $scope.duration, method: "GET", params: $scope.getParams()})
                    .success(function(data, staus, headers, config) {
                    // console.log('success with : ', data);

                        $scope.progress.stop();
                        goog.payments.inapp.buy({
                            'jwt'     : data,
                            'success' : $scope.success,
                            'failure' : $scope.failure
                        });
                        })
	                .error(function(data, status, headers, config) {
	                        console.log('error');
	                })
                ;// end http invocation
				$scope.progress.start();
			}
		}

	};// end function purchase

	$scope.progress = {
		start : function () {
			$scope.progress.dim(0.1);
			$scope.progress.togg(1);
		},
		stop  : function () {
			$scope.progress.dim(1.0);
			$scope.progress.togg(0);
		},
		dim   : function (val) {
			$('.booking').css('opacity', val);
		},
		togg  : function (flag) {
			if (flag) {
			  $('.loading').css('display', 'block');
			} else {
			  $('.loading').css('display', 'none');
			}
		}
	}// end object progress


	$scope.updateFields = function() {
		var departureDate = Date.parse($scope.endModel);
		var arrivalDate   = Date.parse($scope.startModel);

		console.log(arrivalDate, departureDate);

		if (arrivalDate && departureDate) {
			$scope.duration = (new TimeSpan(departureDate - arrivalDate)).days;
			if ($scope.duration == '0') $scope.duration = 1;
			console.log('duration : ',$scope.duration);
			$scope.price = $scope.duration * 50;
		} else {
			$scope.duration = "0";
			$scope.price = "0.00";
		}
	}; // end function updateFields
}// end function PaymentCtrl



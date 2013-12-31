'use strict'

function TourblyCtrl($scope, $window, $http) {

	$scope.apiBase = "/oauth/";
	$scope.revokeUrl = 'https://accounts.google.com/o/oauth2/revoke?token';

	$scope.uDat = {email: "", verified: ""};

	$scope.userData = {
		email      : "",
		gender     : "",
		picture    : "",
		last_name  : "",
		languages  : "",
		activated  : "",
		first_name : ""
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

					$scope.uDat.email     = resp.email;
					$scope.uDat.activated = resp.verified_email;

					$scope.outBound.post({
						url   : "signin",
						async : "false",
						dat   : $scope.uDat
					}).done(function(data) {
						console.log("SUCCESS, POST TO SERVER WITH STATUS: ");
						console.log(data);

						if(data=="notfound") {
							window.location.replace("/signup");
						} else {
							document.cookie=data.split("*-*")[0];
							document.cookie=data.split("*-*")[1];
							location.reload();
						}
					});
				});

			} else if (authResult['error']) {
				console.log('There was an error: ' + authResult['error']);
			}

		});
	};// end function signin

	$scope.signup = function(authResult) {
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

					console.log($scope.userData);
					$scope.outBound.post({
						url   : "signup",
						async : "false",
						dat   : $scope.userData
					}).done(function(data) {
						if(data=="duplicate") {
							window.location.replace("/signin");
						} else {
							document.cookie=data.split("*-*")[0];
							document.cookie=data.split("*-*")[1];
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
		$.ajax({
			type: 'GET',
		    url: $scope.revokeUrl + $scope.accessToken.get(),
		    async: false,
		    contentType: "application/json",
		    dataType: 'jsonp',
		    success: function(nullResponse) {
		    	console.log("Successfully disconnected!");
		    	$scope.accessToken.del();


		    	$http({method: 'POST', url: '/disconnect'}).
		    	  success(function(data, status, headers, config) {
		    	  }).
		    	  error(function(data, status, headers, config) {
		    	  });

		    	$window.alert("Disconnect Successfull");
		    	location.reload();
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
	}// end function disconnect

	$scope.outBound =  {
		get: function(_args) {
			return $.ajax({
				type        : 'GET',
				url         : $scope.apiBase + _args.url,
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
				url         : $scope.apiBase + _args.url,
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


	$window.renderSignup = function() {
		if ($('#signup-form').is(':visible')) {
			gapi.signin.render('customBtn', {
				'callback': $scope.signup,
				'immedediate': false,
				'clientid': '1066634592899-vq0boe9dv5s49lf3jghr6qo825bvesg9.apps.googleusercontent.com',
				'cookiepolicy': 'single_host_origin',
				'requestvisibleactions': 'http://schemas.google.com/AddActivity',
				'scope': 'https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email'
			});
		}

		if ($('#mobile').is(':visible')) {
			gapi.signin.render('customBtn_M', {
				'callback': $scope.signup,
				'immedediate': false,
				'clientid': '1066634592899-vq0boe9dv5s49lf3jghr6qo825bvesg9.apps.googleusercontent.com',
				'cookiepolicy': 'single_host_origin',
				'requestvisibleactions': 'http://schemas.google.com/AddActivity',
				'scope': 'https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email'
			});
		}
	}// end function renderSignup

	$scope.dummy = function() {
		console.log('here is the cookie', $scope.accessToken.get());
	}
	$window.glob = function(){$scope.dummy();}


}// end controller TourblyCtrl

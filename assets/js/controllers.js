'use strict'

function TourblyCtrl($scope, $window) {

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
						async : "false",
						url   : $scope.apiBase,
						dat   : $scope.userData
					}).done(function(data) {
						document.cookie=data.split("*-*")[0];
						document.cookie=data.split("*-*")[1];
						location.reload();
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

		    	$scope.outBound.post({
		    		async : "false",
		    		url   : '/disconnect',
		    	}).done(function(data) {
		    		console.log('Successfully deleted tourist', data);
		    	});

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
	}// end function disconnect

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

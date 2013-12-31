/*
 * Copyright (c) 2013 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */

'use strict';

function NavBarCtrl($scope, Logout, $cookies) {
  $scope.showAuthButs = Logout.showAuthButs;
  $scope.updateShowAuthButs = function(val) {
    Logout.updateShowAuthButs(val);
  };

  $scope.$on( 'Logout.update', function( event, showAuthButs ) {
    $scope.showAuthButs = showAuthButs;
  });

  $scope.logoutCall = function() {
    $scope.updateShowAuthButs(true);
    $cookies.session = '';
  };
}

function TourblyCtrl($scope, $location, Conf, TourblyApi, Logout, $cookies) {

  // signIn
  $scope.userProfile = undefined;
  $scope.hasUserProfile = false;
  $scope.isSignedIn = false;
  $scope.immediateFailed = false;

  $scope.disconnect = function() {
    console.log('disconnect clicked');
    TourblyApi.disconnect().then(function() {
      $scope.userProfile = undefined;
      $scope.hasUserProfile = false;
      $scope.isSignedIn = false;
      $scope.immediateFailed = true;
      Logout.updateShowAuthButs(true);
    });
  }


  $scope.signedIn = function(profile) {
    $scope.isSignedIn = true;
    $scope.userProfile = profile;
    $scope.hasUserProfile = true;
    Logout.updateShowAuthButs(false);
  };



  $scope.signIn = function(authResult) {
    var $authResult = jQuery.extend(true, {}, authResult);
    $scope.$apply(function() {
      $scope.processAuth(jQuery.extend(true, {}, $authResult));
    });
  }

  $scope.processAuth = function(authResult) {
    $scope.immediateFailed = true;
    if ($scope.isSignedIn) {
      return 0;
    }
    if (authResult['access_token']) {
      $scope.immediateFailed = false;
      // Successfully authorized, create session
      TourblyApi.signIn(authResult).then(function(response) {
        $scope.signedIn(response.data);
      });
    } else if (authResult['error']) {
      if (authResult['error'] == 'immediate_failed') {
        $scope.immediateFailed = true;
      } else {
        console.log('Error:' + authResult['error']);
      }
    }
  }

  $scope.renderMobileSignIn = function() {
    gapi.signin.render('customBtn_M', {
      'callback': $scope.signIn,
      'clientid': Conf.clientId,
      'requestvisibleactions': Conf.requestvisibleactions,
      'scope': Conf.scopes,
      'theme': 'dark',
      'cookiepolicy': Conf.cookiepolicy,
      'accesstype': 'offline'
    });
  }

  $scope.renderWebSignIn = function() {
    gapi.signin.render('customBtn', {
      'callback': $scope.signIn,
      'clientid': Conf.clientId,
      'requestvisibleactions': Conf.requestvisibleactions,
      'scope': Conf.scopes,
      'theme': 'dark',
      'cookiepolicy': Conf.cookiepolicy,
      'accesstype': 'offline'
    });
  }

  $scope.renderSignIn = function() {
    if ($('#signup-form').is(':visible')) {
      $scope.renderWebSignIn();
    }

    if ($('#mobile').is(':visible')) {
      $scope.renderMobileSignIn();
    }
  }

  $scope.start = function() {
    $scope.renderSignIn();
    if ($cookies.session) {
      Logout.updateShowAuthButs(false);
    } else Logout.updateShowAuthButs(true);
  }

  $scope.start();

}

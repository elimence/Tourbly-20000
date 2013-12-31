
'use strict'

angular.module('tourbly', ['ngCookies'],
    function($locationProvider) {
      $locationProvider.html5Mode(true);
    }
);

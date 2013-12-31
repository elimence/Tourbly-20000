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

angular.module('tourbly.services', [])
    .factory('Conf', function($location) {
      function getRootUrl() {
        var rootUrl = $location.protocol() + '://' + $location.host();
        if ($location.port())
          rootUrl += ':' + $location.port();
        return rootUrl;
      };
      return {
        'clientId': '1066634592899-vq0boe9dv5s49lf3jghr6qo825bvesg9.apps.googleusercontent.com',
        'apiBase': '/api/',
        'scopes': 'https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email',
        'requestvisibleactions': 'http://schemas.google.com/AddActivity ',
         'cookiepolicy': 'single_host_origin'
      };
    })
    .factory('Logout', function($rootScope) {
      return {
        showAuthButs: true,
        updateShowAuthButs: function(val) {
          this.showAuthButs = val;
          $rootScope.$broadcast( 'Logout.update', this.showAuthButs );
        }
      };
    })
    .factory('TourblyApi', function($http, Conf) {
      return {
        signIn: function(authResult) {
          return $http.post(Conf.apiBase + 'connect', authResult)
        },
        disconnect: function() {
          return $http.post(Conf.apiBase + 'disconnect');
        }
      };
    })
;

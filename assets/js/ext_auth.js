
 var usr_prf_ops = {

    BASE_API_PATH : 'plus/v1/',

    s_up_c_bks    : function(authResult) {
      gapi.client.load('plus', 'v1', function() {
        if (authResult['access_token']) {
          usr_prf_ops.profile();
          usr_prf_ops.people();
        } else if(authResult['error']) {
          console.log('There was an error: ' + authResult['error']);
        }

        console.log('authResult', authResult);
      });
    },

    s_in_c_bks  : function(authResult) {
      if (authResult['access_token']) {
        document.write('signed in successfully with gplus');
      } else if(authResult['error']) {
        console.log('There was an error: ' + authResult['error']);
      }

      console.log('authResult', authResult);
    },

    un_auth_usr : function() {
      $.ajax({
        type        : 'GET',
        url         : 'https://accounts.google.com/o/oauth2/revoke?token=' + gapi.auth.getToken().access_token,
        async       : false,
        contentType : 'application/json',
        dataType    : 'jsonp',

        success     : function(result) {
          console.log('revoke response: ' + result);
        },

        error       : function(e) {
          console.log(e);
        }

      });
    },

    people : function() {
      var request = gapi.client.plus.people.list({
        'userId': 'me',
        'collection': 'visible'
      });

      request.execute(function(people) {
        console.log('Number of people visible to this app: ' + people.totalItems + '\n');
        for (var personIndex in people.items) {
          person = people.items[personIndex];
          console.log(person.image.url);
        }
      });
    },

    profile : function() {
      var request = gapi.client.plus.people.get( {'userId' : 'me'} );
      request.execute( function(profile) {
        if (profile.error) {
          console.log(profile.error);
          return;
        }

        console.log('image: '+ profile.image.url);
        console.log('display name: '+ profile.displayName);
        console.log('tagline: '+ profile.tagline);
        console.log('about me: '+ profile.aboutMe);

        if (profile.cover && profile.coverPhoto) {
          console.log('cover phote: '+ profile.cover.coverPhoto.url);
        }
      });
    }

 } // ends usr_prf_ops

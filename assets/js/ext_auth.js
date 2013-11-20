
 var usr_prf_ops = {

    BASE_API_PATH : 'plus/v1/',

    _aboutMe     : "",
    _tagline     : "",
    _coverPhoto  : "",
    _visiblePpl  : "",
    _profilePic  : "",
    _displayName : "",


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

    }, // end property def s_up_c_bks


    s_in_c_bks  : function(authResult) {
      gapi.client.load('plus', 'v1', function() {
        if (authResult['access_token']) {
          usr_prf_ops.profile();
          usr_prf_ops.people();
        } else if(authResult['error']) {
          console.log('There was an error: ' + authResult['error']);
        }

        console.log('authResult', authResult);
      });

    }, // end property def - s_in_c_bks


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

    }, // end property def un_auth_usr


    people : function() {
      var request = gapi.client.plus.people.list({
        'userId': 'me',
        'collection': 'visible'
      });

      request.execute(function(people) {
        usr_prf_ops._visiblePpl = people.totalItems;

        for (var personIndex in people.items) {
          person = people.items[personIndex];
          console.log(person.image.url);
        }
      });

    }, // end property def - people


    profile : function() {
      var request = gapi.client.plus.people.get( {'userId' : 'me'} );
      request.execute( function(profile) {
        if (profile.error) {
          console.log(profile.error);
          return;
        }

        usr_prf_ops._aboutMe      = profile.aboutMe;
        usr_prf_ops._tagline      = profile.tagline;
        usr_prf_ops._profilePic   = profile.image.url;
        usr_prf_ops._displayName  = profile.displayName;

        console.log(usr_prf_ops);

        if (profile.cover && profile.coverPhoto) {
          usr_prf_ops._coverPhoto = profile.cover.coverPhoto.url;
        }
      });

    } // end property def - profile


 } // end usr_prf_ops


 var to_srv = {

 }

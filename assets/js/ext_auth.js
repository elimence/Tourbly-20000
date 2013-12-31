var access_token = "";

var userData = {
  email      : "",
  gender     : "",
  picture    : "",
  last_name  : "",
  languages  : "",
  activated  : "",
  first_name : ""
};

var uDat = {
  email : "",
  verified : ""
};


var usr_prf_ops = {

  s_up_c_bks    : function(authResult) {

    gapi.client.load('oauth2', 'v2', function() {
      if (authResult['access_token']) {
        gapi.client.oauth2.userinfo.get().execute(function(resp) {
          console.log('from here and now on');
          console.log(resp);
          access_token = authResult['access_token'];
          console.log("here's the access token",authResult['access_token']);
          userData.email     = resp.email;
          userData.activated = resp.verified_email;
        });

      } else if (authResult['error']) {
        console.log('There was an error: ' + authResult['error']);
      }

    });

    gapi.client.load('plus', 'v1', function() {
      if (authResult['access_token']) {
        console.log("here's the access token",authResult['access_token']);
        gapi.client.plus.people.get( {'userId' : 'me'} ).execute(function(resp) {
          // console.log(resp);
          userData.gender     = resp.gender;
          userData.picture    = resp.image.url;
          userData.languages  = resp.language;
          userData.last_name  = resp.name.familyName;
          userData.first_name = resp.name.givenName;

          console.log(userData);
          srv_com_tel.post({
            url   : "/oauth/signup",
            async : "false",
            dat   : userData
          }).done(function(data) {
            console.log("SUCCESS, POST TO SERVER WITH STATUS: ");
            console.log(data);

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

  }, // end property def s_up_c_bks


  s_in_c_bks  : function(authResult) {

    gapi.client.load('oauth2', 'v2', function() {
      if (authResult['access_token']) {
        console.log("here's the access token",authResult['access_token']);
        gapi.client.oauth2.userinfo.get().execute(function(resp) {
          // console.log(resp);
          uDat.email     = resp.email;
          uDat.activated = resp.verified_email;

          srv_com_tel.post({
            url   : "/oauth/signin",
            async : "false",
            dat   : uDat
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

  }, // end property def - s_in_c_bks


  revoke_auth : function() {
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


  sign_out_of_app : function() {
    gapi.auth.signOut();
  },


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


}; // end usr_prf_ops


var srv_com_tel = {
  get   : function(_args) {
    return $.ajax({
      type        : 'GET',
      url         : _args.url,
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

  post  : function(_args) {
    return $.ajax({
      type        : 'POST',
      url         : _args.url,
      async       : _args.async,
      data        : _args.dat
    })
    .fail(function(data) {
      console.log("FAILURE, POST TO SERVER WITH STATUS: ");
      console.log(data);
    });
  },

  submit  : function(_args) {
    $.post (_args.url, _args.data, function(data) {
      console.log("SUCCESS, NON-AJAX POST");
      console.log(data);
    });
  }
};

function pseudoPhotoSelectClickListener (e) {
  e.preventDefault();
  $('#picture-select').click();
}
function actualPhotoSelectClickListener (e) {
}

// function disconnectButtonClickListener(e) {
//   $('#confirmDisconnect').modal();
// }

// function continueWithDisconnectClickListener(e) {
//   if (!($('#newpass').val())) { // If no password was entered
//     var proceed = confirm("If you do not type a password, your Tourbly account will be closed! Are you sure you want to continue?");
//     if (proceed) {
//       // You can disconnect from google and close the account
//     } else {
//       // Do nothing
//     }
//   } else {
//     var pass = $('#newpass').val(),
//         confirmPass = $('#confirm').val();

//     if (!confirmPass) {
//       alert('Please confirm you password');
//     } else if (pass != confirmPass) {
//       alert('Your passwords do not match');
//     } else {
//       // Passwords match so do what you need to do
//     }
//   }
// }

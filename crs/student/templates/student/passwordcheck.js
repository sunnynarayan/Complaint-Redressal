$(document).ready(function() {
$('#password').keyup(function() {
$('#result').html(checkStrength($('#password').val()))
})
function checkStrength(password) {
var strength = 0
<<<<<<< HEAD
if (password.length < 6) {
=======
if (password.length < 8) {
>>>>>>> 402c4d313db5b74172ea6d37dda719bcc223ea92
$('#result').removeClass()
$('#result').addClass('short')
return 'Too short'
}
<<<<<<< HEAD
if (password.length > 7) strength += 1
=======
if (password.length > 8) strength += 1
>>>>>>> 402c4d313db5b74172ea6d37dda719bcc223ea92
// If password contains both lower and uppercase characters, increase strength value.
if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1
// If it has numbers and characters, increase strength value.
if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 1
// If it has one special character, increase strength value.
if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
// If it has two special characters, increase strength value.
if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
// Calculated strength value, we can return messages
// If value is less than 2
<<<<<<< HEAD
if (strength < 2) {
$('#result').removeClass()
$('#result').addClass('weak')
return 'Weak'
} else if (strength == 2) {
$('#result').removeClass()
$('#result').addClass('good')
=======
if (strength < 3) {
$('#result').removeClass()
$('#result').addClass('weak')
return 'Weak'
} else if (strength == 3) {
$('#result').removeClass()
$('#result').addClass('good')
$('#submit').show();
>>>>>>> 402c4d313db5b74172ea6d37dda719bcc223ea92
return 'Good'
} else {
$('#result').removeClass()
$('#result').addClass('strong')
<<<<<<< HEAD
=======
$('#submit').show();
>>>>>>> 402c4d313db5b74172ea6d37dda719bcc223ea92
return 'Strong'
}
}
});
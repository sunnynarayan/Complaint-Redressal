$(document).ready(function() {
$('#password').keypress(function() {
$('#result').html(checkStrength($('#password').val()))
})
function checkStrength(password) {
var strength = 0
if (password.length < 8) {
$('#result').removeClass()
$('#result').addClass('short')
// $('#submit').hide()
return 'Too short'
}
if (password.length >= 8) strength += 1
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

if (strength < 4 &&   ) {
$('#result').removeClass()
$('#result').addClass('weak')
// $('#submit').hide()
return 'Weak'
} else if (strength == 4) {
$('#result').removeClass()
$('#result').addClass('good')
$('#submit').show();
return 'Good'
} else {
$('#result').removeClass()
$('#result').addClass('strong')
$('#submit').show();
return 'Strong'
}

}
});
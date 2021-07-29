$(document).ready(function() {
$('#exerciseType').on('change', function() {
  console.log($('#exerciseType').val());
  $('#teachGoal').html('');
  if ($('#exerciseType').val() == 'fib') {
    $('#teachGoal').append('<option value="present-simple-progr">Present Simple/Progressive</option>');
    $('#teachGoal').append('<option value="past-simple-progr">Past Simple/Progressive</option>');
    $('#teachGoal').append('<option value="present-past-perfect">Present/Past Perfect</option>');
  } else if ($('#exerciseType').val() == 'mistakes'){
    $('#teachGoal').append('<option value="present-simple-progr">Present Simple/Progressive</option>');
    $('#teachGoal').append('<option value="past-simple-progr">Past Simple/Progressive</option>');
//    $('#teachGoal').append('<option value="present-past-perfect">Present/Past Perfect</option>');
  } else if ($('#exerciseType').val() == 'multiple'){
    $('#teachGoal').append('<option value="present-simple-progr">Present Simple/Progressive</option>');
    $('#teachGoal').append('<option value="past-simple-progr">Past Simple/Progressive</option>');
//    $('#teachGoal').append('<option value="present-past-perfect">Present/Past Perfect</option>');
  }
})
});


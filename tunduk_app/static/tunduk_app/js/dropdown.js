$("#type_request_field").change(function() {
  if($(this).val()=='1') {
    $('#pin_field_div').show();
    $('#pin_field').attr('required', '');
    $('#pin_field').attr('data-error', 'Необходимо заполнить это поле');
    $('#phone_number_field_div').show();
    $('#phone_number_field').attr('required', '');
    $('#phone_number_field').attr('data-error');
    $('#birth_date_field_div').show();
    $('#birth_date_field').attr('required', '');
    $('#birth_date_field').attr('data-error');
    $('#issued_date_field_div').show();
    $('#issued_date_field').attr('required', '');
    $('#issued_date_field').attr('data-error');

    $('#code_field_div').hide();
    $('#code_field').removeAttr('required', '');
    $('#code_field').removeAttr('data-error');
    $('#request_id_field_div').hide();
    $('#request_id_field').removeAttr('required', '');
    $('#request_id_field').removeAttr('data-error');

  } else if($(this).val()=='2') {
    $('#code_field_div').show();
    $('#code_field').attr('required', '');
    $('#code_field').attr('data-error', 'Необходимо заполнить это поле');
    $('#request_id_field_div').show();
    $('#request_id_field').attr('required', '');
    $('#request_id_field').attr('data-error', 'Необходимо заполнить это поле');

    $('#pin_field_div').hide();
    $('#pin_field').removeAttr('required', '');
    $('#pin_field').removeAttr('data-error');
    $('#phone_number_field_div').hide();
    $('#phone_number_field').removeAttr('required', '');
    $('#phone_number_field').removeAttr('data-error');
    $('#birth_date_field_div').hide();
    $('#birth_date_field').removeAttr('required', '');
    $('#birth_date_field').removeAttr('data-error');
    $('#issued_date_field_div').hide();
    $('#issued_date_field').removeAttr('required', '');
    $('#issued_date_field').removeAttr('data-error');

  } else if ($(this).val()=='3') {
    $('#pin_field_div').show();
    $('#pin_field').attr('required', '');
    $('#pin_field').attr('data-error', 'Необходимо заполнить это поле');

    $('#code_field_div').hide();
    $('#code_field').removeAttr('required', '');
    $('#code_field').removeAttr('data-error');
    $('#request_id_field_div').hide();
    $('#request_id_field').removeAttr('required', '');
    $('#request_id_field').removeAttr('data-error');
    $('#phone_number_field_div').hide();
    $('#phone_number_field').removeAttr('required', '');
    $('#phone_number_field').removeAttr('data-error');
    $('#birth_date_field_div').hide();
    $('#birth_date_field').removeAttr('required', '');
    $('#birth_date_field').removeAttr('data-error');
    $('#issued_date_field_div').hide();
    $('#issued_date_field').removeAttr('required', '');
    $('#issued_date_field').removeAttr('data-error');
  } else if ($(this).val()=='4') {
    $('#pin_field_div').show();
    $('#pin_field').attr('required', '');
    $('#pin_field').attr('data-error', 'Необходимо заполнить это поле');

    $('#code_field_div').hide();
    $('#code_field').removeAttr('required', '');
    $('#code_field').removeAttr('data-error');
    $('#request_id_field_div').hide();
    $('#request_id_field').removeAttr('required', '');
    $('#request_id_field').removeAttr('data-error');
    $('#phone_number_field_div').hide();
    $('#phone_number_field').removeAttr('required', '');
    $('#phone_number_field').removeAttr('data-error');
    $('#birth_date_field_div').hide();
    $('#birth_date_field').removeAttr('required', '');
    $('#birth_date_field').removeAttr('data-error');
    $('#issued_date_field_div').hide();
    $('#issued_date_field').removeAttr('required', '');
    $('#issued_date_field').removeAttr('data-error');
  }
});
$("#type_request_field").trigger("change");

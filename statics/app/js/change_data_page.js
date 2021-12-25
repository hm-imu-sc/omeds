let password = $('#new_password');
let retype_password = $('#retype_new_password');
let password_ok = false;
let retype_password_ok = false;
let submit = $('#submit');
let date_name = $('#data_name');
let date = new Date();

if($(date_name).val() === "date_of_birth") {
    $('#new_date_of_birth').val(date.toISOString().split('T')[0]);
}

$(password).on('keyup', function () {
    let password_text = $(password).val();
    let password_length = password_text.length;

    let upper_case = false, lower_case = false, digit = false, special_char = false;

    for(let i=0; i<password_length; i++){
        if(password_text[i]>='A' && password_text[i]<='Z'){
            upper_case = true;
        }
        else if (password_text[i]>='a' && password_text[i]<='z') {
            lower_case = true;
        }
        else if (password_text[i]>='0' && password_text[i]<='9') {
            digit = true;
        }
        else  {
            special_char = true;
        }
    }

    console.log(upper_case);
    console.log(lower_case);
    console.log(digit);
    console.log(special_char);
    console.log(password_length);

    if (upper_case && lower_case && digit && special_char && password_length>=6) {

        $(password).removeClass('is-invalid');
        $(password).addClass('is-valid');

        password_ok = true;

        if ($(password).val() === $(retype_password).val()) {
            $(retype_password).removeClass('is-invalid');
            $(retype_password).addClass('is-valid');
            retype_password_ok = true;
        }
        else {
            $(retype_password).removeClass('is-valid');
            $(retype_password).addClass('is-invalid');
            retype_password_ok = false
        }

        if (retype_password_ok) {
            $(submit).attr('disabled', false);
        }
    }
    else {
        $(password).removeClass('is-valid');
        $(password).addClass('is-invalid');

        password_ok = false;

        if ($(password).val() === $(retype_password).val()) {
            $(retype_password).removeClass('is-invalid');
            $(retype_password).addClass('is-valid');
            retype_password_ok = true;
        }
        else {
            $(retype_password).removeClass('is-valid');
            $(retype_password).addClass('is-invalid');
            retype_password_ok = false
        }

        $(submit).attr('disabled', true);
    }
});

$(retype_password).on('keyup', function () {
    if ($(password).val() === $(retype_password).val()) {
        $(retype_password).removeClass('is-invalid');
        $(retype_password).addClass('is-valid');
        retype_password_ok = true;

        console.log(password_ok);

        if (password_ok) {
            $(submit).attr('disabled', false);
        }
    }
    else {
        $(retype_password).removeClass('is-valid');
        $(retype_password).addClass('is-invalid');
        retype_password_ok = false;
        $(submit).attr('disabled', true);
    }
});
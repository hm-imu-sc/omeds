let password = $('#password');
let retype_password = $('#retype_password');
let date = new Date();
let user_type = $('#user_type');
let submit = $('#submit');
let password_ok = false;
let retype_password_ok = false;
let user_type_ok = false;
let pass_prev_len = 0;

function initial_check() {
    if ($(user_type).val() === 'null') {
        user_type_ok = false;
    }
    else {
        user_type_ok = true;
    }

    // pass_check

    let password_text = $(password).val();
    let password_length = password_text.length;

    if (password_length === 0) {
        return;
    }

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
        else {
            special_char = true;
        }
    }

    if (upper_case && lower_case && digit && special_char && password_length>=6) {
        $(password).removeClass('is-invalid');
        $(password).addClass('is-valid');

        password_ok = true;
    }
    else {
        $(password).removeClass('is-valid');
        $(password).addClass('is-invalid');

        password_ok = false;
    }

    // repass check

    if ($(password).val() === $(retype_password).val()) {
        $(retype_password).removeClass('is-invalid');
        $(retype_password).addClass('is-valid');
        retype_password_ok = true;

        if (password_ok && user_type_ok) {
            $(submit).attr('disabled', false);
        }
    }
    else {
        $(retype_password).removeClass('is-valid');
        $(retype_password).addClass('is-invalid');
        retype_password_ok = false;
    }
}

$(user_type).on('change', function () {
    if($(user_type).val() === 'null') {
        $(submit).attr('disabled', true);
        user_type_ok = false;
    }
    else {
        if(password_ok && retype_password_ok){
            $(submit).attr('disabled', false);
        }
        // console.log("[+] User typer changed !!!")
        user_type_ok = true;
    }
});

$('#date_of_birth').val(date.toISOString().split('T')[0]);

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
        else if (password_length>pass_prev_len) {
            special_char = true;
        }
        else {
            pass_prev_len = password_length;
        }
    }

    // console.log(upper_case);
    // console.log(lower_case);
    // console.log(digit);
    // console.log(special_char);
    // console.log(password_length);

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

        if (user_type_ok && retype_password_ok) {
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

        if (password_ok && user_type_ok) {
            $(submit).attr('disabled', false);
        }
    }
    else {
        $(retype_password).removeClass('is-valid');
        $(retype_password).addClass('is-invalid');
        retype_password_ok = false
        $(submit).attr('disabled', true);
    }
});

initial_check();

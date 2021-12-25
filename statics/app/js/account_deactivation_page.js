let password = $('#password');
let retype_password = $('#retype_password');
let submit = $('#submit');

function password_mismatch_check() {
    if ($(password).val() === $(retype_password).val()) {
        $(retype_password).removeClass('is-invalid');
        $(password).removeClass('is-invalid');
        $(password).addClass('is-valid');
        $(retype_password).addClass('is-valid');

        $(submit).attr('disabled', false);
    }
    else {
        $(password).removeClass('is-valid');
        $(retype_password).removeClass('is-valid');
        $(password).addClass('is-invalid');
        $(retype_password).addClass('is-invalid');

        $(submit).attr('disabled', true);
    }
}

$(password).on('keyup', password_mismatch_check);
$(retype_password).on('keyup', password_mismatch_check);
from django.shortcuts import render
from django.db import connection
from argon2 import PasswordHasher
from django.http import HttpResponseRedirect
from django.urls import reverse
from my_modules import page_works, exceptions
import datetime

cursor = connection.cursor()
hasher = PasswordHasher()

# Create your views here.


def test_page(request):

    data_dict = {
        'page_name': 'test_page',
        'login_status': 'false',
    }

    try:
        page_works.get_active_user(request)
    except:
        data_dict['login_status'] = 'false'

    return render(request, 'app/test_page.html', context=data_dict)


def view_database_page(request):
    table_names = [
        'patient',
        'doctor',
        'session',
    ]

    data_dict = {
        'page_name': 'view_database_page',
        'table_names': table_names,
    }

    try:
        page_works.request_verify(request, False)
        data_dict['login_status'] = 'false'
    except exceptions.LogoutRequiredException:
        user_dict = page_works.get_active_user(request)
        data_dict['logged_in_username'] = user_dict['name']
        data_dict['user_type'] = user_dict['user_type']
        data_dict['login_status'] = 'true'

    return render(request, 'app/view_database_page.html', data_dict)


def view_table_page(request, table_name):
    command = (
        "SELECT * FROM {}".format(table_name)
    )
    cursor.execute(command)

    table = list(cursor.fetchall())

    command = (
        "SELECT UPPER(COLUMN_NAME) " +
        "FROM INFORMATION_SCHEMA.COLUMNS " +
        "WHERE TABLE_NAME = '{}' ".format(table_name) +
        "ORDER BY ORDINAL_POSITION "
    )
    cursor.execute(command)
    column_names = list(cursor.fetchall())

    data_dict = {
        'page_name': 'view_database_page',
        'table_name': table_name,
        'column_names': column_names,
        'table': table,
    }

    try:
        page_works.request_verify(request, False)
        data_dict['login_status'] = 'false'
    except exceptions.LogoutRequiredException:
        user_dict = page_works.get_active_user(request)
        data_dict['logged_in_username'] = user_dict['name']
        data_dict['user_type'] = user_dict['user_type']
        data_dict['login_status'] = 'true'

    return render(request, 'app/view_table_page.html', data_dict)


def landing_page(request):

    data_dict = {
        'page_name': 'landing_page',
        'login_status': 'false',
    }

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    return render(request, 'app/landing_page.html', context=data_dict)


def registration_page(request):

    data_dict = {
        'page_name': 'registration_page',
        'login_status': 'false',
    }

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    return render(request, 'app/registration_page.html', context=data_dict)


def registration(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    if request.method == 'GET':
        return registration_page(request)

    user_type = request.POST.get('user_type')
    name = request.POST.get('name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    mobile_no = request.POST.get('mobile_no')
    password = request.POST.get('password')
    retype_password = request.POST.get('retype_password')
    date_of_birth = request.POST.get('date_of_birth')
    gender = request.POST.get('gender')
    enc_pass = hasher.hash(password)

    if user_type == 'doctor':
        user = "doctor"
    else:
        user = "patient"

    command = (
        "SELECT COUNT(username) " +
        "FROM doctor " +
        "WHERE username LIKE '{}'".format(username)
    )
    cursor.execute(command)
    count_username = int(cursor.fetchall()[0][0])
    command = (
        "SELECT COUNT(username) " +
        "FROM patient " +
        "WHERE username LIKE '{}'".format(username)
    )
    cursor.execute(command)
    count_username += int(cursor.fetchall()[0][0])

    command = (
        "SELECT COUNT(username) " +
        "FROM patient " +
        "WHERE email LIKE '{}'".format(email)
    )
    cursor.execute(command)
    count_email = int(cursor.fetchall()[0][0])
    command = (
        "SELECT COUNT(username) " +
        "FROM doctor " +
        "WHERE email LIKE '{}'".format(email)
    )
    cursor.execute(command)
    count_email += int(cursor.fetchall()[0][0])

    command = (
        "SELECT COUNT(username) " +
        "FROM doctor " +
        "WHERE mobile_number LIKE '{}'".format(mobile_no)
    )
    cursor.execute(command)
    count_mobile_no = int(cursor.fetchall()[0][0])
    command = (
        "SELECT COUNT(username) " +
        "FROM patient " +
        "WHERE mobile_number LIKE '{}'".format(mobile_no)
    )
    cursor.execute(command)
    count_mobile_no += int(cursor.fetchall()[0][0])

    alerts = []
    valid = True

    if count_username > 0:
        alerts.append("Username is not available !")
        valid = False
    if count_email > 0:
        alerts.append("'{}' is already associated with another account !".format(email))
        valid = False
    if count_mobile_no > 0:
        alerts.append("'{}' is already associated with another account !".format(mobile_no))
        valid = False

    if not valid:
        data_dict = {
            'name': name,
            'username': username,
            'email': email,
            'mobile_no': mobile_no,
            # 'password': password,
            # 'retype_password': retype_password,
            'date_of_birth': date_of_birth,
            'alerts': alerts,
            'page_name': 'registration_page',
            'login_status': 'false',
        }

        return render(request, 'app/registration_page.html', context=data_dict)

    command = (
        "INSERT INTO {}".format(user) +
        "(name, username, email, mobile_number, enc_pass, date_of_birth, gender) " +
        "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(name, username, email, mobile_no, enc_pass, date_of_birth, gender)
    )

    # print("[+] COMMAND: {}".format(command))

    cursor.execute(command)

    return HttpResponseRedirect(reverse('app:successfull_page'))


def successfull_page(request):

    data_dict = {
        'page_name': 'successfull_page',
        'login_status': 'false',
    }

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    return render(request, 'app/successfull_page.html', context=data_dict)


def login_page(request, alerts=[]):

    data_dict = {
        'page_name': 'login_page',
        'login_status': 'false',
        'alerts': alerts,
    }

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    return render(request, 'app/login_page.html', context=data_dict)


def login(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    if request.method == 'GET':
        return login_page(request)

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = "null"

    command = (
        "SELECT COUNT(username) " +
        "FROM doctor " +
        "WHERE username LIKE '{}'".format(username)
    )
    cursor.execute(command)
    if int(cursor.fetchall()[0][0]) == 1:
        user = 'doctor'
    else:
        command = (
            "SELECT COUNT(username) " +
            "FROM patient " +
            "WHERE username LIKE '{}'".format(username)
        )
        cursor.execute(command)
        if int(cursor.fetchall()[0][0]) == 1:
            user = 'patient'

    if user == 'null':
        alerts = ["No associated account found with username: '{}' !!!".format(username)]
        return login_page(request, alerts)

    command = (
        "SELECT enc_pass " +
        "FROM {} ".format(user) +
        "WHERE username LIKE '{}'".format(username)
    )
    cursor.execute(command)
    enc_pass = cursor.fetchall()[0][0]

    try:
        password_verified = hasher.verify(enc_pass, password)
    except:
        password_verified = False

    if password_verified:

        command = (
            "UPDATE {} ".format(user) +
            "SET status='active'" +
            "WHERE username LIKE '{}'".format(username)
        )
        cursor.execute(command)

        command = (
            "SELECT name FROM {} ".format(user) +
            "WHERE username LIKE '{}'".format(username)
        )
        cursor.execute(command)

        name = cursor.fetchall()[0][0]

        command = (
            "INSERT INTO session (username, expires, user_type) " +
            "VALUES ('{}', DATE_ADD(NOW(), INTERVAL 3 DAY), '{}')".format(username, user)
        )
        cursor.execute(command)

        command = (
            "SELECT MAX(id) FROM session"
        )
        cursor.execute(command)

        session_id = int(cursor.fetchall()[0][0])

        cookie_content = "{}{}{}".format(session_id, username, enc_pass)
        cookie_content = hasher.hash(cookie_content)
        cookie_content = "{}_{}".format(session_id, cookie_content)

        cookie_expires = datetime.datetime.now() + datetime.timedelta(hours=66)
        cookie_expires = cookie_expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

        data_dict = {
            'logged_in_username': name,
            'user_type': user,
            'login_status': 'true',
        }

        if user == 'patient':
            data_dict['page_name'] = 'patient_home_page'
            response = render(request, 'app/patient_home_page.html', context=data_dict)
        else:
            data_dict['page_name'] = 'doctor_home_page'
            response = render(request, 'app/doctor_home_page.html', context=data_dict)

        response.set_cookie('_login_session', cookie_content, expires=cookie_expires)

        return response
    else:
        alerts = ["Credential didn't match !!!"]
        data_dict = {
            'alerts': alerts,
            'username': username,
            'page_name': 'login_page',
            'login_status': 'false',
        }
        return render(request, 'app/login_page.html', context=data_dict)


def logout(request):
    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    session_id = user_dict['session_id']

    command = (
        "DELETE FROM session WHERE session.id={}".format(session_id)
    )
    cursor.execute(command)

    return login_page(request)


def manage_account_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'login_status': 'true',
        'page_name': 'manage_account_page',
    }

    return page_works.extend_session(request, render(request, 'app/manage_account_page.html', context=data_dict))


def account_deactivation_page(request, alerts=[]):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'login_status': 'true',
        'page_name': 'account_deactivation_page',
        'alerts': alerts,
    }

    return render(request, 'app/account_deactivation_page.html', context=data_dict)


def account_deactivation(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'login_status': 'true',
    }

    password = request.POST.get('password')

    command = (
        "SELECT enc_pass " +
        "FROM {} ".format(user_dict['user_type']) +
        "WHERE username LIKE '{}'".format(user_dict['username'])
    )
    cursor.execute(command)
    enc_pass = cursor.fetchall()[0][0]

    try:
        hasher.verify(enc_pass, password)
    except:
        return account_deactivation_page(request, ["Password didn't match !!!"])

    command = (
        "UPDATE {} ".format(user_dict['user_type']) +
        "SET status='deactive' " +
        "WHERE username LIKE '{}'".format(user_dict['username'])
    )
    cursor.execute(command)

    command = (
        "DELETE FROM session WHERE username LIKE '{}'".format(user_dict['username'])
    )
    cursor.execute(command)

    return login_page(request, ['Your account has been deactivated !!! Please login to activate your account.'])


def account_deletion_page(request, alerts=[]):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'login_status': 'true',
        'page_name': 'account_deletion_page',
        'alerts': alerts,
    }

    return render(request, 'app/account_deletion_page.html', context=data_dict)


def account_deletion(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'login_status': 'true',
    }

    password = request.POST.get('password')

    command = (
        "SELECT enc_pass " +
        "FROM {} ".format(user_dict['user_type']) +
        "WHERE username LIKE '{}'".format(user_dict['username'])
    )
    cursor.execute(command)
    enc_pass = cursor.fetchall()[0][0]

    try:
        hasher.verify(enc_pass, password)
    except:
        return account_deactivation_page(request, ["Password didn't match !!!"])

    command = (
        "DELETE FROM {} ".format(user_dict['user_type']) +
        "WHERE username LIKE '{}'".format(user_dict['username'])
    )
    cursor.execute(command)

    command = (
        "DELETE FROM session " +
        "WHERE username LIKE '{}'".format(user_dict['username'])
    )
    cursor.execute(command)

    return login_page(request, alerts=['Your account has been deleted !!!'])


def patient_home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'page_name': 'patient_home_page',
        'login_status': 'true',
    }

    return render(request, 'app/patient_home_page.html', context=data_dict)


def patient_profile_page(request, alerts=[]):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    command = (
        "SELECT name, username, email, mobile_number, DATE_FORMAT(date_of_birth, '%d %M, %Y'), gender " +
        "FROM {} ".format(user_dict['user_type']) +
        "WHERE username LIKE '{}'".format(user_dict['username'])
    )
    cursor.execute(command)

    user_data = list(cursor.fetchall()[0])

    user_data = [
        ['Name :', user_data[0], 'name'],
        ['Username :', user_data[1], 'username'],
        ['Email :', user_data[2], 'email'],
        ['Mobile number :', user_data[3], 'mobile_number'],
        ['Date of Birth :', user_data[4], 'date_of_birth'],
        ['Gender :', user_data[5], 'gender'],
    ]

    data_dict = {
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'user_data': user_data,
        'alerts': alerts,
        'page_name': 'patient_profile_page',
        'login_status': 'true',
    }

    return render(request, 'app/patient_profile_page.html', context=data_dict)


def doctor_home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'page_name': 'doctor_home_page',
        'login_status': 'true',
    }

    return render(request, 'app/doctor_home_page.html', context=data_dict)


def doctor_profile_page(request, alerts=[]):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    command = (
        "SELECT name, username, email, mobile_number, DATE_FORMAT(date_of_birth, '%d %M, %Y'), gender " +
        "FROM {} ".format(user_dict['user_type']) +
        "WHERE username LIKE '{}'".format(user_dict['username'])
    )
    cursor.execute(command)

    user_data = list(cursor.fetchall()[0])

    user_data = [
        ['Name :', user_data[0], 'name'],
        ['Username :', user_data[1], 'username'],
        ['Email :', user_data[2], 'email'],
        ['Mobile number :', user_data[3], 'mobile_number'],
        ['Date of Birth :', user_data[4], 'date_of_birth'],
        ['Gender :', user_data[5], 'gender'],
    ]

    data_dict = {
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'user_data': user_data,
        'alerts': alerts,
        'page_name': 'doctor_profile_page',
        'login_status': 'true',
    }

    return render(request, 'app/doctor_profile_page.html', context=data_dict)


def home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    if user_dict['user_type'] == 'patient':
        return patient_home_page(request)
    else:
        return doctor_home_page(request)


def profile_page(request, alerts=[]):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    if user_dict['user_type'] == 'patient':
        return patient_profile_page(request, alerts)
    else:
        return doctor_profile_page(request, alerts)


def change_data_page(request, data_name='null', current_data='null', alerts=[]):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    header = ''

    if data_name == 'name':
        header = 'Name'
    elif data_name == 'username':
        header = 'Username'
    elif data_name == 'email':
        header = 'Email'
    elif data_name == 'mobile_number':
        header = 'Mobile Number'
    elif data_name == 'date_of_birth':
        header = 'Date of Birth'
    elif data_name == 'gender':
        header = 'Gender'
    elif data_name == 'password':
        header = 'Password'
    else:
        return profile_page(request)

    data_dict = {
        'alerts': alerts,
        'header': header,
        'data_name': data_name,
        'current_data': current_data,
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'page_name': 'change_{}_page'.format(data_name),
        'login_status': 'true',
    }

    return render(request, 'app/change_data_page.html', context=data_dict)


def change_data(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    user_type = user_dict['user_type']
    username = user_dict['username']

    command = (
        "SELECT enc_pass " +
        "FROM {} ".format(user_type) +
        "WHERE username LIKE '{}'".format(username)
    )
    cursor.execute(command)

    enc_pass = cursor.fetchall()[0][0]
    password = request.POST.get('password')

    data_name = request.POST.get('data_name')
    current_data = request.POST.get('current_data')
    new_data = request.POST.get('new_data')

    try:
        hasher.verify(enc_pass, password)
    except:
        alerts = ['Wrong password !!!']
        return change_data_page(request, data_name, current_data, alerts)

    if data_name == 'username' or data_name == 'email' or data_name == 'mobile_number':

        command = (
            "SELECT COUNT(username) " +
            "FROM doctor " +
            "WHERE {} LIKE '{}' ".format(data_name, new_data)
        )
        cursor.execute(command)
        count = int(cursor.fetchall()[0][0])
        command = (
            "SELECT COUNT(username) " +
            "FROM patient " +
            "WHERE {} LIKE '{}'".format(data_name, new_data)
        )
        cursor.execute(command)
        count += int(cursor.fetchall()[0][0])

        if count > 0:
            alerts = []

            if data_name == 'username':
                alerts.append("'{}' is not available !!!".format(new_data))
            else:
                alerts.append("'{}' is already associated with another account !!!".format(new_data))

            return change_data_page(request, data_name, current_data, alerts)

        if data_name == 'username':
            command = (
                "UPDATE session " +
                "SET username='{}'".format(new_data) +
                "WHERE username LIKE '{}'".format(username)
            )
            cursor.execute(command)

    elif data_name == 'password':
        data_name = 'enc_pass'
        new_data = hasher.hash(new_data)

    command = (
        "UPDATE {} ".format(user_type) +
        "SET {}='{}'".format(data_name, new_data) +
        "WHERE username LIKE '{}'".format(username)
    )
    cursor.execute(command)

    return profile_page(request, ['Updates saved successfully !!!'])

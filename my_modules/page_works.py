import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OMEDS.settings')
import django
django.setup()


from django.db import connection
from my_modules import exceptions
from argon2 import PasswordHasher
import datetime


cursor = connection.cursor()
hasher = PasswordHasher()


def get_session_id(request):
    cookie_content = request.COOKIES.get('_login_session')

    try:
        session_id = cookie_content.split('_')[0]
    except:
        session_id = -1

    return session_id


def request_verify(request, login_required):

    session_id = get_session_id(request)

    command = (
        "SELECT COUNT(username) " +
        "FROM session " +
        "WHERE id={}".format(session_id)
    )
    cursor.execute(command)
    count = int(cursor.fetchall()[0][0])

    if login_required and count == 0:
        raise exceptions.LoginRequiredException
    elif not login_required and count > 0:
        raise exceptions.LogoutRequiredException
    else:
        return True


def get_active_user(request):

    session_id = get_session_id(request)

    command = (
        "SELECT username, user_type " +
        "FROM session " +
        "WHERE id={}".format(session_id)
    )
    cursor.execute(command)
    query_data = cursor.fetchall()[0]

    command = (
            "SELECT name FROM {} ".format(query_data[1]) +
            "WHERE username LIKE '{}'".format(query_data[0])
    )
    cursor.execute(command)

    name = cursor.fetchall()[0][0]

    user_data = {
        'username': query_data[0],
        'user_type': query_data[1],
        'name': name,
        'session_id': session_id,
    }

    command = (
        "DELETE FROM session WHERE expires<NOW() AND username LIKE '{}'".format(user_data['username'])
    )
    cursor.execute(command)

    return user_data


def extend_session(request, response):
    session_id = get_session_id(request)
    user_data = get_active_user(request)

    command = (
        "DELETE FROM session " +
        "WHERE id={}".format(session_id)
    )
    cursor.execute(command)

    command = (
        "INSERT INTO session (username, expires, user_type) " +
        "VALUES ('{}', DATE_ADD(NOW(), INTERVAL 3 DAY), '{}')".format(user_data['username'], user_data['user_type'])
    )
    cursor.execute(command)

    command = (
        "SELECT MAX(id) FROM session"
    )
    cursor.execute(command)

    session_id = int(cursor.fetchall()[0][0])

    command = (
        "SELECT enc_pass FROM {} ".format(user_data['user_type']) +
        "WHERE username LIKE '{}'".format(user_data['username'])
    )
    cursor.execute(command)

    enc_pass = cursor.fetchall()[0][0]

    cookie_content = "{}{}{}".format(session_id, user_data['username'], enc_pass)
    cookie_content = hasher.hash(cookie_content)
    cookie_content = "{}_{}".format(session_id, cookie_content)

    cookie_expires = datetime.datetime.now() + datetime.timedelta(hours=66)
    cookie_expires = cookie_expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie('_login_session', cookie_content, expires=cookie_expires)

    return response

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OMEDS.settings')
import django
django.setup()


from django.db import connection
from faker import Faker
from random import choice
from argon2 import PasswordHasher


cursor = connection.cursor()
faker = Faker()
hasher = PasswordHasher()


def get_mobile_no():

    sim_codes = '015 017 019 018 016'.split(' ')
    digits = '0 1 2 3 4 5 6 7 8 9'.split(' ')

    mobile_no = choice(sim_codes)

    for i in range(8):
        mobile_no += str(choice(digits))

    return mobile_no


def get_common_data():
    password = faker.password(length=6, special_chars=True, digits=True, upper_case=True, lower_case=True),
    # print("TYPE: {}".format(type(password[0])))
    try:
        enc_pass = hasher.hash(password[0])
    except:
        raise Exception("NOT OK !!!")

    data_dict = {
        'username': faker.user_name(),
        'email': faker.ascii_free_email(),
        'password': password[0],
        'enc_pass': enc_pass,
        'name': faker.name(),
        'mobile_number': get_mobile_no(),
        'date_of_birth': faker.date(),
        'status': choice(['active', 'deactive'])
    }

    return data_dict


def populate_doctor(number_of_doctor):

    file = open('doctors.txt', 'a')
    file_cred = open('credentials.txt', 'a')

    while number_of_doctor != 0:

        common_data = get_common_data()
        speciality = choice(['Cardiologists',
                            'Eye',
                            'Medicine',
                            'Skin',
                            'Neurologists',
                            'Immunologists',
                            'Dermatologists',
                            'Gastroenterologists',
                            'Hematologists',
                            'Internists',
                            'Nephrologists',
                            'Osteopaths',
                            'Pathologists',
                            'Physiatrists',
                            'Plastic Surgeons'
                            'Psychiatrists'
                            'Radiologists',
                            'Pulmonologists'
                            ])
        visit_fee = choice([400, 500, 600, 800, 1000])
        balance = choice([5000, 3500, 3654, 10000, 1500, 2000, 4000, 6000, 0])

        gender = choice(['male', 'female'])

        command = (
            "INSERT INTO doctor " +
            "VALUES (" +
            "'{}',".format(common_data['username']) +
            "'{}',".format(common_data['email']) +
            "'{}',".format(common_data['enc_pass']) +
            "'{}',".format(common_data['name']) +
            "'{}',".format(common_data['mobile_number']) +
            "'{}',".format(common_data['date_of_birth']) +
            "'{}',".format(speciality) +
            "{},".format(visit_fee) +
            "{},".format(balance) +
            "'{}',".format(gender) +
            "'{}'".format(common_data['status']) +
            ")"
        )
        try:
            cursor.execute(command)
            number_of_doctor -= 1
            file.write(command+';\n')
            file_cred.write('{}, {}\n'.format(common_data['username'], common_data['password']))
            command = ("delete from doctor where username like '{}'".format(common_data['username']))
            cursor.execute(command)
        except:
            print("[+] --> COMMAND: {}".format(command))

    file.close()
    file_cred.close()


def populate_patient(number_of_patient):

    file = open('patients.txt', 'a')
    file_cred = open('credentials.txt', 'a')

    while number_of_patient != 0:

        common_data = get_common_data()

        balance = choice([5000, 3500, 3654, 10000, 1500, 2000, 4000, 6000, 0])

        gender = choice(['male', 'female'])

        command = (
            "INSERT INTO patient " +
            "VALUES (" +
            "'{}',".format(common_data['username']) +
            "'{}',".format(common_data['email']) +
            "'{}',".format(common_data['enc_pass']) +
            "'{}',".format(common_data['name']) +
            "'{}',".format(common_data['mobile_number']) +
            "'{}',".format(common_data['date_of_birth']) +
            "{},".format(balance) +
            "'{}',".format(gender) +
            "'{}'".format(common_data['status']) +
            ")"
        )
        try:
            cursor.execute(command)
            number_of_patient -= 1
            file.write(command+';\n')
            file_cred.write('{}, {}\n'.format(common_data['username'], common_data['password']))
            command = ("delete from patient where username like '{}'".format(common_data['username']))
            cursor.execute(command)
        except:
            print("[+] --> COMMAND: {}".format(command))

    file.close()
    file_cred.close()

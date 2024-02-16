from faker import Faker
import json
import random

fake = Faker('ru_RU')

data = {}
i = 1
while i < 301:
    gender = ['male', 'female']
    random_gender = random.choice(gender)

    if random_gender == 'male':
        name = fake.first_name_male()
        surname = fake.last_name_male()
        patronymic = ''
        while len(patronymic) == 0:
            fio = fake.name().split()
            for part_name in fio:
                if part_name[-3:] == 'вич':
                    patronymic = part_name

    else:
        name = fake.first_name_female()
        surname = fake.last_name_female()
        patronymic = ''
        while len(patronymic) == 0:
            fio = fake.name().split()
            for part_name in fio:
                if part_name[-3:] == 'вна':
                    patronymic = part_name

    organization = 'organization_example'
    while len(organization) >= 14:
        organization = fake.company()

    data[i] = {
        'name': name,
        'surname': surname,
        'patronymic': patronymic,
        'organization': organization,
        'work_phone': random.randrange(10000000000, 100000000000),
        'personal_phone': random.randrange(10000000000, 100000000000)
    }
    i += 1

my_file = open('test3.txt', "w")
json.dump(data, my_file)
my_file.close()

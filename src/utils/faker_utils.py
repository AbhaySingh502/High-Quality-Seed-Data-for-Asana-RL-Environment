from faker import Faker
fake = Faker()


def fake_name():
    return fake.name()


def fake_email(name, domain):
    username = name.lower().replace(" ", ".")
    return f"{username}@{domain}"


def fake_sentence():
    return fake.sentence()


def fake_paragraph():
    return fake.paragraph()

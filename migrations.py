from models import db, Person
from faker import Factory
import random
from helpers import generate_unique_filename

fake = Factory.create()
# Spanish
#fake = Factory.create('es_ES')
# Reload tables
db.drop_all()
db.create_all()
# Make 100 fake contacts
for num in range(5):
    fullname = fake.name().split()
    name = fullname[0]
    surname = ' '.join(fullname[1:])
    email = fake.email()
    phone = fake.phone_number()
    role = random.choice(['Captain','First officer','Flight attendant'])
    attachment = generate_unique_filename(name,surname)

    # Save in database
    person = Person(name=name, surname=surname, email=email, phone=phone, role=role, attachment=attachment)
    db.session.add(person)

db.session.commit()
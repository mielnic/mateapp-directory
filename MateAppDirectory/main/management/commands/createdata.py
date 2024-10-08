import random
from django.core.management.base import BaseCommand
from faker import Faker
from directory.models import Address, Company, Person
from posts.models import Post

try:
    alid = Address.objects.last().id
    clid = Company.objects.last().id
    plid = Person.objects.last().id

except:
    alid = 0
    clid = 0
    plid = 0

class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        for _ in range(15):
            street = fake.street_address()
            city = fake.city()
            state = fake.state()
            country = fake.country()
            postalCode = fake.postcode()
            Address.objects.create(street=street, state=state, country=country, city=city, postalCode=postalCode)

        for _ in range(15):
            companyName = fake.company()
            tax_id = fake.ein()
            website = fake.domain_name()
            companyPhone = fake.basic_phone_number()
            companyNotes = fake.paragraph(nb_sentences=2, variable_nb_sentences=True)
            aid = alid + random.randint(1,15)
            address = Address.objects.get(id=aid)
            Company.objects.create(companyName=companyName, tax_id=tax_id, website=website, companyPhone=companyPhone, companyNotes=companyNotes, address=address)

        for _ in range(50):
            lastName = fake.last_name()
            firstName = fake.first_name()
            celphone = fake.basic_phone_number()
            workphone = fake.basic_phone_number()
            email = fake.ascii_company_email()
            position = fake.job()
            notes = fake.paragraph(nb_sentences=2, variable_nb_sentences=True)
            aid = alid + random.randint(1,15)
            cid = clid + random.randint(1,15)
            address = Address.objects.get(id=aid)
            company = Company.objects.get(id=cid)
            Person.objects.create(lastName=lastName, firstName=firstName, celphone=celphone, workphone=workphone, email=email, position=position, notes=notes, address=address, company=company)

        for _ in range(100):
            post = fake.paragraph(nb_sentences=2, variable_nb_sentences=True)
            cid = clid + random.randint(1,15)
            company = Company.objects.get(id=cid)
            Post.objects.create(post=post, company=company)
        
        for _ in range(200):
            post = fake.paragraph(nb_sentences=2, variable_nb_sentences=True)
            pid = plid + random.randint(1,50)
            person = Person.objects.get(id=pid)
            Post.objects.create(post=post, person=person)


        print('SUCCESS!')


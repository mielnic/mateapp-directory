from django.test import TestCase
from .models import Person, Company, Address

# Create your tests here.

class PersonTestCase(TestCase):
    def setUp(self):
        address = Address.objects.create(
            street = 'Balcarce 50',
            postalCode = '1000',
            city = 'Buenos Aires',
            state = 'CABA',
            country = 'Argentina'
        )
        company = Company.objects.create(
            companyName = 'Presidencia de la Nación',
            tax_id = '30-66666666-6',
            address = address,
            website = 'https://www.argentina.gob.ar/presidencia',
            companyPhone = '9876-5432',
            companyNotes = 'Mafia'
        )
        Person.objects.create(
            lastName = 'Pérez',
            firstName = 'Juan',
            celphone = '1234-5678',
            email = 'juan.perez@hotmail.com',
            position = 'vendedor',
            notes = 'Juan es un ladrón.',
            company = company
        )

    def test_person_input(self):
        person = Person.objects.get(lastName = 'Pérez')
        # self.assertEqual(person.firstName, 'Juan')
        a = [person.firstName, 
             person.celphone, 
             person.email,
             person.position, 
             person.notes, 
             person.company.companyName, 
             person.company.tax_id, 
             person.company.address.street, 
             person.company.website, 
             person.company.companyPhone, 
             person.company.companyNotes
             ]
        b =['Juan',
            '1234-5678',
            'juan.perez@hotmail.com',
            'vendedor',
            'Juan es un ladrón.',
            'Presidencia de la Nación',
            '30-66666666-6',
            'Balcarce 50',
            'https://www.argentina.gob.ar/presidencia',
            '9876-5432',
            'Mafia'
            ]
        self.assertListEqual(a,b)
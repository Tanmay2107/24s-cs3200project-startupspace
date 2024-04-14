from faker import Faker
fake = Faker()

name = fake.first_name()

print(name)

address = fake.address()


print(address)
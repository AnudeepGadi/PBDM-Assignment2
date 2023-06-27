from faker import Faker
from book import Book
import random

# Create an instance of Faker
fake = Faker()

# Define the list of genres
genres = ['Fiction', 'Mystery', 'Science Fiction', 'Romance']

# Generate additional books using Faker and random values
additional_books = [
    Book(
        isbn=fake.isbn13(),
        title=fake.sentence(),
        author=fake.name(),
        date=fake.date(),
        publisher=fake.company(),
        category=random.choice(genres),
        quantity=fake.random_int(min=1, max=100),
        price=fake.random.uniform(10.0, 100.0)
    )
    for _ in range(10)
]

# Insert the additional books into the collection
result = Book.collection.insert_many([book.__dict__ for book in additional_books])

# Print the IDs of the inserted documents
print(result.inserted_ids)

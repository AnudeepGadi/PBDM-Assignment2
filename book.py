from pymongo import MongoClient, UpdateOne

class Book:
    # MongoDB connection setup - to connect to the cluster library
    client = MongoClient("mongodb+srv://library.yyrfjcb.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority",
                         tls=True,
                         tlsCertificateKeyFile='X509-cert-3769800919841790503.pem')

    # Database and collection setup
    db = client['bookstore']
    collection = db['books']

    def __init__(self, isbn="", title="", author="", date="", publisher="", category="", quantity="", price="", **kwargs):
        # Book attributes initialization
        self.isbn = isbn
        self.title = title
        self.author = author
        self.date = date
        self.publisher = publisher
        self.category = category
        self.quantity = quantity
        self.price = price

    def save(self):
        # Save the book object to the collection
        document = self.__dict__
        result = self.__class__.collection.insert_one(document)
        return result

    @classmethod
    def find(cls, **kwargs):
        # The "find" method retrieves books based on the provided filters, returning results for each matched filter.
        # Adjusting the query from '$or' to '$and' ensures that the results are returned only when all filters are matched.
        filters = [{key: {"$regex": str(value), "$options": "i"}} for key, value in kwargs.items()]
        query = {'$or': filters}
        results = cls.collection.find(query)
        books = [cls(**result) for result in results]
        return books

    @classmethod
    def bulkUpdate(cls, checkout_books):
        # Perform bulk update on books collection based on checkout books
        update_operations = [
            UpdateOne({"isbn": book.isbn}, {"$inc": {"quantity": - quantity}}) for book, quantity in checkout_books
        ]
        result = cls.collection.bulk_write(update_operations)
        print("Number of books updated:", result.modified_count)

    def __str__(self) -> str:
        # String representation of the book object
        return f"ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Date: {self.date}, \
                Publisher: {self.publisher}, Category: {self.category}, Quantity: {self.quantity}, Price: {self.price}"

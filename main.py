from functools import reduce
from book import Book
from tabulate import tabulate

# Function to print a table of books
def printTable(books):
    headers = ['ISBN', 'Title', 'Author', 'Date', 'Publisher', 'Category', 'Available Quantity', 'Price']
    table_data = [[book.isbn, book.title, book.author, book.date, book.publisher, book.category, book.quantity, book.price] for book in books]
    table = tabulate(table_data, headers=headers, tablefmt='grid')
    print(table)

# Function to print a table of books in the cart
def printCart(books):
    headers = ['ISBN', 'Title', 'Author', 'Category', 'Quantity', 'Price Per Book', 'Total Price']
    table_data = [[book.isbn, book.title, book.author, book.category, quantity, book.price, quantity*book.price ] for (book,quantity) in books]
    table = tabulate(table_data, headers=headers, tablefmt='grid', showindex="always")
    print(table)    

# Function to add a book to the library
def addBook():
    isbn = input("ISBN: ")
    title = input("Title: ")
    author = input("Author: ")
    date = input("Date: ")
    publisher = input("Publisher: ")
    category = input("Category: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: "))

    book = Book(isbn, title, author, date, publisher, category, quantity, price)
    result = book.save()
    print(f" The inserted book id is is {result.inserted_id}")

# Function to search for books based on user input
def searchBooks():
    print("You can press Enter to skip any field.\nIf at least one field matches, the corresponding record will be displayed.")
    title = input("Title: ") or None
    author = input("Author: ") or None
    category = input("Category: ") or None
    isbn = input("ISBN: ") or None
    books = Book.find(author = author ,title = title, isbn = isbn, category=category)
    printTable(books)

# Function to perform the checkout process
def checkOut():
    checkout_books = []
    while True:
        print("--"*20)
        print(f"1. Add book to cart\n2. Confirm checkout\n3. Cancel")
        try:
            sub_choice = int(input("Please enter your option : "))
        except Exception as e:
            print("Wrong choice entered")
        
        if sub_choice == 1:
            isbn = input("enter isbn number : ")
            books = list(Book.find(isbn = isbn))
            if len(books) > 0: 
                printTable(books)
                qunatity = int(input("Enter quantity : "))
                if qunatity < 1:
                    print("Quantity should be greater than 1")
                    continue
                book = books[0]
                if qunatity > book.quantity:
                    print("The entered quantity exceeds the available quantity in the library.")
                else:
                    checkout_books.append((book,qunatity))
                    print(f"Book '{book.title}' with quantity {qunatity} has been successfully added to your cart.")
                    print("\nItems in your cart")
                    printCart(checkout_books)     
            else: 
                print("No results found")
        
        elif sub_choice == 2:
            if len(checkout_books)>0:
                print("Please check the items in you cart")
                printCart(checkout_books)
                total_sum = reduce(lambda total, book_tuple: total + (book_tuple[0].price * book_tuple[1]), checkout_books, 0)
                print("Total Sum:", total_sum) 
                while True:
                    print("--"*20)
                    print("1. Confirm\n2. Cancel")        
                    try:
                        confirm_choice = int(input("Please enter your option: "))  
                    except Exception as e:
                        print("Wrong choice entered") 
                    if confirm_choice == 1:
                        Book.bulkUpdate(checkout_books)
                        print("Transaction Successful")
                        break
                    elif confirm_choice == 2:
                        checkout_books = []
                        break
                    else:
                        print("Invalid option entered")                
            else:
                print("Cart empty")
        
        elif sub_choice == 3:
            checkout_books = []
            break

        else:
            print("Invalid option entered")

# Main program loop
if __name__ == "__main__":
    while True:
        print("--" * 20)
        print("1. Add Book\n2. Search Book\n3. Checkout\n4. Quit")
        try:
            choice = int(input("Please enter your option: "))
        except Exception as e:
            print("Wrong choice entered")
        
        if choice == 1:
            # Option 1: Add a book
            addBook()
        
        elif choice == 2:
            # Option 2: Search for books
            searchBooks()

        elif choice == 3:
            # Option 3: Perform checkout
            checkOut()
        
        elif choice == 4:
            # Option 4: Quit the program
            break

        else:
            print("Invalid option entered")

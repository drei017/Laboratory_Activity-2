================================================================
  LIBRARY BOOK TRACKER — Program Reflection & Questions
================================================================


----------------------------------------------------------------
QUESTION 1:
Explain the overall design of your program and justify why you
chose this particular class structure and set of user-defined
methods.
----------------------------------------------------------------

The program uses two classes: Book and Library.

Book represents a single book with three attributes — title,
author, and is_borrowed — and handles its own behavior through
the borrow(), return_book(), and get_status() methods.

Library acts as the manager, holding a list of Book objects and
providing methods to add, find, and display them.

This structure was chosen because it mirrors how a real library
works — a library organizes books, while each book manages its
own state. Keeping these responsibilities separate makes the
code cleaner and easier to expand in the future.


----------------------------------------------------------------
QUESTION 2:
Describe how user input is handled in your program and discuss
the role of exception handling (try–except) in preventing
incorrect or unexpected behavior.
----------------------------------------------------------------

User input is collected through QLineEdit fields in the PyQt6
GUI. When the user submits an action, a try–except block catches
any errors and displays a toast notification instead of crashing.

Exceptions are raised in four situations: blank input, a book
title that doesn't exist, borrowing a book that's already taken,
and returning a book that was never borrowed. Each case gives the
user a clear, specific error message so they always know what
went wrong.


----------------------------------------------------------------
QUESTION 3:
Identify one limitation of your current implementation and
explain how it could be improved using additional OOP concepts
or better error handling.
----------------------------------------------------------------

The biggest limitation is that data doesn't persist — closing
the app resets everything back to the three default books.

This could be fixed by adding a third class, LibraryStorage,
responsible solely for saving and loading book data to a file.
This keeps each class focused on one job: Book manages book
behavior, Library manages the collection, and LibraryStorage
handles the file. Switching to a database later would only
require changes to LibraryStorage, leaving the other classes
untouched.

================================================================

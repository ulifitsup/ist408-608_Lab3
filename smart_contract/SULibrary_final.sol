// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract SULibrary {
    
    // Structure representing a library member
    struct member {
        string member_name;       // Name of the member
        bool member_active;       // True if member is active, false if inactive
        book[2] borrowed_books;   // Array of books borrowed by the member, max 2 books
        uint borrowed_count;      // Count of books currently borrowed
    }

    // Structure representing a book in the library
    struct book {
        string book_name;         // Name/title of the book
        bool book_status;         // True if available, false if currently lent out
    }

    // Mapping of books by ISBN
    mapping (string => book) private books;
    // Mapping of members by their unique member ID
    mapping (string => member) private members;

    // Registers a new member with a name and unique member ID
    function member_register(string memory name, string memory member_id) public {
        members[member_id].member_name = name;
        members[member_id].member_active = true;
        members[member_id].borrowed_count = 0;

        // Initialize borrowed_books array for the new member
        for (uint i = 0; i < 2; i++) {
            members[member_id].borrowed_books[i] = book("", true);
        }
    }
    
    // Deactivates a member, making them inactive in the system
    function member_deactive(string memory member_id) public {
        members[member_id].member_active = false;
    }

    // Adds a new book to the library by ISBN and book name
    function new_book(string memory book_name, string memory ISBN) public {
        require(bytes(books[ISBN].book_name).length == 0, "Book with this ISBN already exists!");
        books[ISBN] = book(book_name, true); // New books are marked as available
    }

    // Allows a member to borrow a book by specifying their ID and the book's ISBN
    function borrow_book(string memory member_id, string memory ISBN) public {
        require(members[member_id].member_active, "Member is not active");       // Check if member is active
        require(books[ISBN].book_status, "Book is not available");               // Check if book is available

        member storage borrower = members[member_id];
        require(borrower.borrowed_count < 2, "Cannot borrow more than 2 books"); // Ensure the member hasn't reached the borrowing limit

        books[ISBN].book_status = false;                                        // Mark the book as lent
        borrower.borrowed_books[borrower.borrowed_count] = books[ISBN];         // Add book to the member's borrowed list
        borrower.borrowed_count++;                                              // Increase the count of borrowed books
    }

    // Allows a member to return a borrowed book by specifying their ID and the book's ISBN
    function return_book(string memory member_id, string memory ISBN) public {
        member storage borrower = members[member_id];
        bool bookFound = false; // Flag to track if the book is found in the borrowed list

        // Search for the book in the member's borrowed list
        for (uint i = 0; i < borrower.borrowed_count; i++) {
            if (keccak256(abi.encodePacked(borrower.borrowed_books[i].book_name)) == keccak256(abi.encodePacked(books[ISBN].book_name))) {
                books[ISBN].book_status = true; // Mark the book as available again
                borrower.borrowed_books[i] = borrower.borrowed_books[borrower.borrowed_count - 1]; // Remove the book from borrowed list
                borrower.borrowed_books[borrower.borrowed_count - 1] = book("", true); // Clear the last borrowed slot
                borrower.borrowed_count--; // Decrease the borrowed count
                bookFound = true;
                break;
            }
        }
        
        require(bookFound, "Book not found in borrowed list"); // Ensure the book was in the borrowed list
    }

    // Retrieves member information by member ID
    function get_member(string memory member_id) view public returns(member memory){
        require(members[member_id].member_active, "Member is not active"); // Ensure the member is active
        return members[member_id];
    }

    // Retrieves book information by ISBN
    function get_book(string memory ISBN) view public returns(book memory){
        return books[ISBN];
    }
}

-- Library Management System Database
-- Database creation
DROP DATABASE IF EXISTS library_management;
CREATE DATABASE library_management;
USE library_management;

-- Members table
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    membership_date DATE NOT NULL,
    membership_status ENUM('active', 'expired', 'suspended') DEFAULT 'active',
    CONSTRAINT chk_email CHECK (email LIKE '%@%.%')
);

-- Authors table
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(50),
    biography TEXT
);

-- Publishers table
CREATE TABLE publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(100)
);

-- Books table
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    publisher_id INT,
    publication_year INT,
    edition INT,
    category VARCHAR(50),
    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 1,
    shelf_location VARCHAR(20),
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON DELETE SET NULL,
    CONSTRAINT chk_copies CHECK (available_copies <= total_copies AND available_copies >= 0)
);

-- Book-Author relationship (many-to-many)
CREATE TABLE book_authors (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

-- Loans table
CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status ENUM('checked_out', 'returned', 'overdue') DEFAULT 'checked_out',
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    CONSTRAINT chk_dates CHECK (due_date >= loan_date AND (return_date IS NULL OR return_date >= loan_date))
);

-- Fines table
CREATE TABLE fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    issue_date DATE NOT NULL,
    payment_date DATE,
    status ENUM('unpaid', 'paid') DEFAULT 'unpaid',
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id) ON DELETE CASCADE,
    CONSTRAINT chk_amount CHECK (amount > 0)
);

-- Insert sample data
-- Publishers
INSERT INTO publishers (name, address, phone, email, website) VALUES
('Penguin Random House', '1745 Broadway, New York, NY 10019', '212-782-9000', 'info@penguinrandomhouse.com', 'https://www.penguinrandomhouse.com'),
('HarperCollins', '195 Broadway, New York, NY 10007', '212-207-7000', 'contact@harpercollins.com', 'https://www.harpercollins.com'),
('Simon & Schuster', '1230 Avenue of the Americas, New York, NY 10020', '212-698-7000', 'info@simonandschuster.com', 'https://www.simonandschuster.com');

-- Authors
INSERT INTO authors (first_name, last_name, birth_date, nationality, biography) VALUES
('George', 'Orwell', '1903-06-25', 'British', 'Eric Arthur Blair, better known by his pen name George Orwell, was an English novelist, essayist, journalist, and critic.'),
('J.K.', 'Rowling', '1965-07-31', 'British', 'Joanne Rowling, better known by her pen name J.K. Rowling, is a British author, philanthropist, film producer, and screenwriter.'),
('Stephen', 'King', '1947-09-21', 'American', 'Stephen Edwin King is an American author of horror, supernatural fiction, suspense, crime, science-fiction, and fantasy novels.');

-- Members
INSERT INTO members (first_name, last_name, email, phone, address, membership_date, membership_status) VALUES
('John', 'Doe', 'john.doe@example.com', '555-123-4567', '123 Main St, Anytown, USA', '2022-01-15', 'active'),
('Jane', 'Smith', 'jane.smith@example.com', '555-987-6543', '456 Oak Ave, Somewhere, USA', '2022-03-22', 'active'),
('Robert', 'Johnson', 'robert.j@example.com', '555-555-1212', '789 Pine Rd, Nowhere, USA', '2022-05-10', 'suspended');

-- Books
INSERT INTO books (title, isbn, publisher_id, publication_year, edition, category, total_copies, available_copies, shelf_location) VALUES
('1984', '978-0451524935', 1, 1949, 1, 'Dystopian', 5, 3, 'A12'),
('Animal Farm', '978-0451526342', 1, 1945, 1, 'Satire', 3, 2, 'A13'),
('Harry Potter and the Sorcerer''s Stone', '978-0590353427', 2, 1997, 1, 'Fantasy', 7, 5, 'B22'),
('The Shining', '978-0307743657', 3, 1977, 1, 'Horror', 4, 4, 'C15');

-- Book-Author relationships
INSERT INTO book_authors (book_id, author_id) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 3);

-- Loans
INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date, status) VALUES
(1, 1, '2023-01-10', '2023-01-24', '2023-01-20', 'returned'),
(2, 2, '2023-02-15', '2023-03-01', NULL, 'overdue'),
(3, 1, '2023-03-05', '2023-03-19', NULL, 'checked_out');

-- Fines
INSERT INTO fines (loan_id, amount, issue_date, payment_date, status) VALUES
(2, 5.50, '2023-03-02', NULL, 'unpaid'),
(1, 2.00, '2023-01-21', '2023-01-25', 'paid');
PRAGMA foreign_keys = ON;

-- 1 --
CREATE TABLE IF NOT EXISTS Books (
    id_books INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Author TEXT NOT NULL
);

-- 2 --
CREATE TABLE IF NOT EXISTS Borrowers (
    id_borrowers INTEGER PRIMARY KEY AUTOINCREMENT,
    Family_name TEXT NOT NULL,
    First_name TEXT NOT NULL,
    contact_phone_number TEXT
);

-- 3 --
CREATE TABLE IF NOT EXISTS Loans (
    id_loans INTEGER PRIMARY KEY AUTOINCREMENT,
    Book INTEGER NOT NULL,
    Borrower INTEGER NOT NULL,
    loan_date TEXT NOT NULL,
    FOREIGN KEY (Book) REFERENCES Books(id_books) ON DELETE CASCADE,
    FOREIGN KEY (Borrower) REFERENCES Borrowers(id_borrowers) ON DELETE CASCADE
);


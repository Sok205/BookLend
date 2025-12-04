-- 1 --
SELECT
    L.id_loans AS id_loan,
    B.Title,
    B.Author,
    Bw.Family_name,
    substr(Bw.First_name, 1, 1) || '.' AS initial_name,
    L.loan_date AS date_of_loan
FROM Loans L
JOIN Books B ON L.Book = B.id_books
JOIN Borrowers Bw ON L.Borrower = Bw.id_borrowers;

-- 2 --
SELECT
    B.id_books,
    B.Title,
    B.Author,
    L.id_loans,
    L.loan_date
FROM Loans L
JOIN Books B ON L.Book = B.id_books
JOIN Borrowers Bw ON L.Borrower = Bw.id_borrowers
WHERE Bw.Family_name = :family_name;

-- 3 --
SELECT
    B.id_books,
    B.Title,
    B.Author,
    COUNT(L.id_loans) AS times_borrowed
FROM Books B
LEFT JOIN Loans L ON B.id_books = L.Book
GROUP BY B.id_books, B.Title, B.Author
ORDER BY times_borrowed DESC;

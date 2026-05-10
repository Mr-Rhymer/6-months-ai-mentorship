SELECT FirstName, LastName, City FROM Customers ORDER BY LastName ASC;

SELECT COUNT(*) FROM Invoices WHERE Total > 10;

SELECT BillingCountry, COUNT(*) FROM Invoices GROUP BY BillingCountry ORDER BY COUNT(*) DESC;

SELECT Composer, COUNT(*) FROM Tracks GROUP BY Composer ORDER BY COUNT(*) DESC LIMIT 10;

SELECT GenreId, AVG(Milliseconds) FROM Tracks GROUP BY GenreId ORDER BY AVG(Milliseconds) DESC;
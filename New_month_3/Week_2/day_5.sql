/*Create a single SQL query that answers this business question:

"For each customer, show their full name, total amount spent, the number of invoices, the last purchase date, and their support employee's full name. Only include customers who have spent more than $10. Order by total spent descending."*/

SELECT 
c.FirstName AS C_FIRSTNAME,
c.LastName AS C_LASTNAME,
sum(i.Total) AS TOTAL_SPENT,
MAX(i.InvoiceDate) AS LastPurchaseDATE,
COUNT(i.InvoiceId) AS NUMBER_OF_INVOICES,
e.FirstName||' '|| e.LastName AS SupportRep
FROM customers c
JOIN invoices i
ON c.CustomerId = i.CustomerId
JOIN employees e
on e.EmployeeId = c.SupportRepId
GROUP BY c.CustomerId HAVING TOTAL_SPENT > 10
ORDER BY TOTAL_SPENT DESC
;
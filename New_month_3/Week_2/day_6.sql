/*Answer this question using SQL:

"Which artist has generated the most revenue? Show artist name and total revenue."*/

SELECT 
artists.name as  Artist_Name,
sum(invoice_items.UnitPrice * invoice_items.Quantity) as total_revenue
from invoice_items
join tracks
on invoice_items.TrackId = tracks.TrackId
join albums
on tracks.AlbumId = albums.AlbumId
join artists
on artists.ArtistId = albums.ArtistId 
group by artists.ArtistId order by total_revenue desc limit 1
;
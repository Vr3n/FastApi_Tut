SELECT post.*, COUNT(votes.post_id) AS votes FROM post LEFT JOIN votes ON post.id = votes.post_id 
WHERE post.id = 4 GROUP BY post.id;
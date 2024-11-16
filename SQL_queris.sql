--1
SELECT rest_name, rating
FROM alberta
WHERE rating > (SELECT AVG(rating) FROM alberta);

--2
SELECT rest_name, food_type, number_of_reviews
FROM manitoba
ORDER BY number_of_reviews DESC
LIMIT 5;

--3Top 5 restaurants by rating
SELECT rest_name, rating
FROM ontario
ORDER BY rating DESC
LIMIT 5;

--4
-- Top 5 restaurants by rating
SELECT rest_name, rating
FROM quebec
ORDER BY rating DESC
LIMIT 5;

--5
SELECT food_type, AVG(rating) AS avg_rating
FROM vancouver
GROUP BY food_type
ORDER BY avg_rating DESC;

--6 Using CTE for Average Rating by Food Type and Filtering Top Restaurants

WITH AvgRatings AS (
    SELECT food_type, AVG(rating) AS avg_rating
    FROM alberta
    GROUP BY food_type
)
SELECT R.rest_name, R.rating, AR.avg_rating
FROM alberta R
JOIN AvgRatings AR ON R.food_type = AR.food_type
WHERE R.rating > AR.avg_rating
LIMIT 10;

--7 Using CTE to Rank Restaurants by Number of Reviews
WITH RankedRestaurants AS (
    SELECT rest_name, number_of_reviews, 
           RANK() OVER (ORDER BY number_of_reviews DESC) AS review_rank
    FROM ontario
)
SELECT * FROM RankedRestaurants
WHERE review_rank <= 5;

--8Using Subquery to Calculate the Highest Rated Restaurant for Each Food Type
SELECT rest_name, food_type, rating
FROM alberta R
WHERE rating = (
    SELECT MAX(rating)
    FROM alberta
    WHERE food_type = R.food_type);
	
--9. Restaurants with Above-Average Service and Ambience Ratings
WITH avg_ratings AS (
    SELECT food_type, AVG(service) AS avg_service, AVG(ambience) AS avg_ambience
    FROM alberta
    GROUP BY food_type
)
SELECT r.rest_name, r.food_type, r.service, r.ambience
FROM alberta r
JOIN avg_ratings ar ON r.food_type = ar.food_type
WHERE r.service > ar.avg_service AND r.ambience > ar.avg_ambience;	


-- 10 Review Distribution
WITH review_distribution AS (
    SELECT rest_name, number_of_reviews,
           CASE
               WHEN number_of_reviews < 50 THEN '< 50'
               WHEN number_of_reviews BETWEEN 50 AND 100 THEN '50-100'
               WHEN number_of_reviews BETWEEN 101 AND 200 THEN '101-200'
               ELSE '> 200'
           END AS review_range
    FROM ontario
)
SELECT review_range, COUNT(*) AS restaurant_count
FROM review_distribution
GROUP BY review_range; 

--11 Find restaurants that have the same rating across food, service, ambience
SELECT rest_name, rating, food, service, ambience
FROM quebec
WHERE food = service AND service = ambience AND ambience = rating;

--12Using CTE to Calculate the Average Rating and Compare Each Restaurant
WITH AvgRating AS (
    SELECT AVG(rating) AS avg_rating
    FROM alberta
)
SELECT rest_name, rating,
       CASE
           WHEN rating > (SELECT avg_rating FROM AvgRating) THEN 'Above Average'
           ELSE 'Below Average'
       END AS rating_comparison
FROM alberta;

--13 Find the top 5 most popular food types based on number of reviews, and average rating for each
SELECT food_type, SUM(number_of_reviews) AS total_reviews, AVG(rating) AS avg_rating
FROM alberta
GROUP BY food_type
ORDER BY total_reviews DESC
LIMIT 5;

--14 Highest Value for Money
SELECT rest_name, coupon, value,
       RANK() OVER (PARTITION BY coupon ORDER BY value DESC) AS rank
FROM quebec;

--15 Find Restaurants with the Highest Service Rating in Each Food Type (Subquery)
SELECT rest_name, food_type, service
FROM alberta R1
WHERE service = (
    SELECT MAX(service)
    FROM alberta R2
    WHERE R1.food_type = R2.food_type
);

--16
WITH HighRated AS (
    SELECT rest_name, rating
    FROM vancouver
    WHERE rating >= 4.5
)
SELECT HR.rest_name, HR.rating, R.number_of_reviews
FROM HighRated HR
JOIN vancouver R ON HR.rest_name = R.rest_name
WHERE R.number_of_reviews > 500;

--17 Using CTE for Average Rating by Food Type and Filtering Top Restaurants

WITH AvgRatings AS (
    SELECT food_type, AVG(rating) AS avg_rating
    FROM alberta
    GROUP BY food_type
)
SELECT R.rest_name, R.rating, AR.avg_rating
FROM alberta R
JOIN AvgRatings AR ON R.food_type = AR.food_type
WHERE R.rating > AR.avg_rating
LIMIT 10;


--18 Using CTE to Rank Restaurants by Number of Reviews
WITH RankedRestaurants AS (
    SELECT rest_name, number_of_reviews, 
           RANK() OVER (ORDER BY number_of_reviews DESC) AS review_rank
    FROM alberta
)
SELECT * FROM RankedRestaurants
WHERE review_rank <= 5;

--19 Using Subquery to Calculate the Highest Rated Restaurant for Each Food Type
SELECT rest_name, food_type, rating
FROM alberta R
WHERE rating = (
    SELECT MAX(rating)
    FROM alberta
    WHERE food_type = R.food_type);
	

 --20. Restaurants with Above-Average Service and Ambience Ratings
WITH avg_ratings AS (
    SELECT food_type, AVG(service) AS avg_service, AVG(ambience) AS avg_ambience
    FROM alberta
    GROUP BY food_type
)
SELECT r.rest_name, r.food_type, r.service, r.ambience
FROM alberta r
JOIN avg_ratings ar ON r.food_type = ar.food_type
WHERE r.service > ar.avg_service AND r.ambience > ar.avg_ambience;
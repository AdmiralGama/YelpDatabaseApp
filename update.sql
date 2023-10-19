DROP TABLE IF EXISTS new_review_count;
DROP TABLE IF EXISTS new_num_checkins;
DROP TABLE IF EXISTS new_reviewRating;

-- review_count
SELECT COUNT(review_id) as new_count INTO new_review_count FROM business NATURAL JOIN review GROUP BY business_id;
UPDATE business
SET review_count = new_count FROM new_review_count;

-- num_checkins
SELECT SUM(count) as new_count INTO new_num_checkins FROM checkin NATURAL JOIN business GROUP BY business_id;
UPDATE business
SET num_checkins = new_count FROM new_num_checkins;

-- reviewRating
SELECT AVG(review_stars) as new_rating INTO new_reviewRating FROM business NATURAL JOIN review GROUP BY business_id;
UPDATE business
SET reviewRating = new_rating FROM new_reviewRating;
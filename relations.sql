DROP TABLE IF EXISTS checkin;
--DROP TABLE IF EXISTS attribute;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS business;
DROP TABLE IF EXISTS zipcodedata;
--DROP TABLE IF EXISTS user;

CREATE TABLE business (business_id CHAR(22), name VARCHAR(100), state CHAR(2), city VARCHAR(50), zipcode VARCHAR(5), address VARCHAR(200), review_count INTEGER, num_checkins INTEGER, reviewRating FLOAT, stars FLOAT, PRIMARY KEY (business_id));
CREATE TABLE checkin (business_id CHAR(22), day VARCHAR(9), time CHAR(5), count INTEGER, FOREIGN KEY (business_id) REFERENCES business (business_id));
--CREATE TABLE attribute (business_id CHAR(22), attr_name VARCHAR(30), value INTEGER, PRIMARY KEY (business_id), FOREIGN KEY (business_id) REFERENCES business (business_id));
CREATE TABLE category (business_id CHAR(22), category_name VARCHAR(50), FOREIGN KEY (business_id) REFERENCES business (business_id));
--CREATE TABLE user (user_id CHAR(22), name VARCHAR(30), fans INTEGER, PRIMARY KEY (user_id));
CREATE TABLE review (review_id CHAR(22), business_id CHAR(22), review_stars FLOAT, text VARCHAR(2000), useful_vote INTEGER, funny_vote INTEGER, cool_vote INTEGER, PRIMARY KEY (review_id), FOREIGN KEY (business_id) REFERENCES business (business_id));
CREATE TABLE zipcodedata (zipcode VARCHAR(5), medianIncome INTEGER, meanIncome INTEGER, population INTEGER, PRIMARY KEY (zipcode));

--in review later once I fix it: user_id CHAR(22), FOREIGN KEY (user_id) REFERENCES user (user_id)
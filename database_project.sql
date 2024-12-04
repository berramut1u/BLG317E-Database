CREATE DATABASE moviebase;
USE moviebase;

CREATE TABLE director
(director_id	int,
 director_name	varchar(100),
 primary key (director_id));
 
CREATE TABLE star
(star_id		int,
 star_name		varchar(100),
 primary key (star_id));
 
CREATE TABLE country
(country_id		int,
 country_name	varchar(20),
 primary key (country_id));
 
CREATE TABLE genre
(genre_id		int,
 genre_name		varchar(20),
 primary key (genre_id));
 
CREATE TABLE production
(production_id	int,
 company_name	varchar(50),
 budget			int,
 gross			int,
 primary key (production_id));
 
CREATE TABLE ratings
(ratings_id			int,
 ratings_category	varchar(5),
 score				double,
 votes				int,
 primary key (ratings_id));

CREATE TABLE movies
(movie_id		int,
 movie_name		varchar(100),
 movie_year 	int,
 runtime		double,
 director_id	int,
 star_id		int,
 country_id 	int,
 genre_id		int,
 production_id	int,
 ratings_id		int,
 primary key (movie_id),
 foreign key (director_id) references director (director_id),
 foreign key (star_id) references star (star_id),
 foreign key (country_id) references country (country_id),
 foreign key (genre_id) references genre (genre_id),
 foreign key (production_id) references production (production_id),
 foreign key (ratings_id) references ratings (ratings_id))
 
 
 

 
  
 
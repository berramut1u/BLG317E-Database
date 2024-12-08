CREATE DATABASE letterboxd;
USE letterboxd;

CREATE TABLE movies
(id					int,
 movie_name			varchar(100),
 movie_date			year,
 tagline			varchar(200) DEFAULT NULL,
 movie_description	varchar(500) DEFAULT NULL,
 movie_length		int,
 movie_rating		double,
 primary key (id));
 
CREATE TABLE actors
(id			int,
 actor_name	varchar(100),
 actor_role	varchar(100) DEFAULT NULL,
 foreign key (id) references movies (id));
 
CREATE TABLE countries
(id			int,
 country	varchar(50),
 foreign key (id) references movies (id));
 
CREATE TABLE crew
(id			int,
 crew_role	varchar(50),
 crew_name	varchar(100),
 foreign key (id) references movies (id));
 
CREATE TABLE genres
(id		int,
 genre	varchar(50),
 foreign key (id) references movies (id));
 
CREATE TABLE languages
(id				int,
 language_type	varchar(50),
 film_language	varchar(50),
 foreign key (id) references movies (id));
 
CREATE TABLE posters
(id		int,
 link	text,
 foreign key (id) references movies (id));
 
CREATE TABLE studios
(id		int,
 studio	varchar(100),
 foreign key (id) references movies (id));
 
CREATE TABLE themes
(id		int,
 theme	varchar(200),
 foreign key (id) references movies (id))
DROP TABLE IF EXISTS show CASCADE;
DROP TABLE IF EXISTS venue CASCADE;
DROP TABLE IF EXISTS artist CASCADE;

CREATE TABLE show (
    id int,
    artist_id int,
    venue_id int,
    start_time timestamp,
    CONSTRAINT pk_show PRIMARY KEY (
        id
     )
);

CREATE TABLE venue (
    id int,
    name varchar(120),
    city varchar(120),
    state varchar(120),
    address varchar(120),
    phone varchar(120),
    genres varchar(120),
    facebook_link varchar(120),
    image_link varchar(200),
    website_link varchar(120),
    looking_for_talent bool,
    seeking_description varchar(500),
    past_shows_count int,
    upcoming_shows_count int,
    CONSTRAINT pk_venue PRIMARY KEY (
        id
     )
);

CREATE TABLE artist (
    id int,
    name varchar(120),
    city varchar(120),
    state varchar(120),
    address varchar(120),
    phone varchar(120),
    genres varchar(120),
    facebook_link varchar(120),
    image_link varchar(200),
    website_link varchar(120),
    looking_for_venues bool,
    seeking_description varchar(500),
    past_shows_count int,
    upcoming_shows_count int,
    CONSTRAINT pk_artist PRIMARY KEY (
        id
     )
);

ALTER TABLE show ADD CONSTRAINT fk_show_artist_id FOREIGN KEY(artist_id)
REFERENCES artist (id);

ALTER TABLE show ADD CONSTRAINT fk_show_venue_id FOREIGN KEY(venue_id)
REFERENCES venue (id);
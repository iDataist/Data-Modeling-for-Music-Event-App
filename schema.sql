DROP TABLE IF EXISTS show CASCADE;
DROP TABLE IF EXISTS venue CASCADE;
DROP TABLE IF EXISTS artist CASCADE;

CREATE TABLE show (
    id serial,
    artist_id int,
    venue_id int,
    start_time timestamp,
    CONSTRAINT pk_show PRIMARY KEY (
        id
     )
);

CREATE TABLE venue (
    id serial,
    name varchar(120),
    city varchar(120),
    state varchar(120),
    address varchar(120),
    phone varchar(120),
    genre varchar(120),
    facebook_link varchar(120),
    image_link varchar(200),
    website_link varchar(120),
    seeking_talent bool,
    seeking_description varchar(500),
    CONSTRAINT pk_venue PRIMARY KEY (
        id
     )
);

CREATE TABLE artist (
    id serial,
    name varchar(120),
    city varchar(120),
    state varchar(120),
    address varchar(120),
    phone varchar(120),
    genre varchar(120),
    facebook_link varchar(120),
    image_link varchar(200),
    website_link varchar(120),
    seeking_venue bool,
    seeking_description varchar(500),
    CONSTRAINT pk_artist PRIMARY KEY (
        id
     )
);

ALTER TABLE show ADD CONSTRAINT fk_show_artist_id FOREIGN KEY(artist_id)
REFERENCES artist (id);

ALTER TABLE show ADD CONSTRAINT fk_show_venue_id FOREIGN KEY(venue_id)
REFERENCES venue (id);
INSERT INTO artist(
	name, city, state, address, phone, genre, facebook_link, image_link, website_link, seeking_venue, seeking_description)
	VALUES 
        (
		'Guns N Petals',
		'San Francisco',
		'CA',
		NULL,
		'326-123-5000',
		'Rock n Roll',
		'https://www.facebook.com/GunsNPetals',
		'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
		'https://www.gunsnpetalsband.com',
		True,
		'Looking for shows to perform at in the San Francisco Bay Area!'
		),
		(
		'Matt Quevedo',
		'New York',
		'NY',
		NULL,
		'300-400-5000',
		'Jazz',
		'https://www.facebook.com/mattquevedo923251523',
		'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
		NULL,
		False,
		NULL
		),
		(
		'The Wild Sax Band',
		'San Francisco',
		'CA',
		NULL,
		'432-325-5432',
		'Jazz',
		NULL,
		'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
		NULL,
		False,
		NULL
		);

INSERT INTO venue(
	name, city, state, address, phone, genre, facebook_link, image_link, website_link, seeking_talent, seeking_description)
	VALUES 
		(
		'The Musical Hop', 
		'San Francisco', 
		'CA',
		'1015 Folsom Street',
		'123-123-1234',
		'Jazz',
		'https://www.facebook.com/TheMusicalHop',
		'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
		'https://www.themusicalhop.com',
		True, 
		'We are on the lookout for a local artist to play every two weeks. Please call us.'
		),
		(
		'The Dueling Pianos Bar',
		'New York',
		'NY',
		'335 Delancey Street',
		'914-003-1132',
		'Classical',
		'https://www.facebook.com/theduelingpianos',
		'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
		'https://www.theduelingpianos.com',
		False,
		NULL
		),
		(
		'Park Square Live Music & Coffee',
		'San Francisco',
		'CA',
		'34 Whiskey Moore Ave',
		'415-000-1234',
		'Rock n Roll',
		'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
		'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
		'https://www.parksquarelivemusicandcoffee.com',
		False,
		NULL
		);

INSERT INTO show(
	artist_id, venue_id, start_time)
	VALUES
		(1, 1, '2019-05-21T21:30:00.000Z'),
		(2, 3, '2019-06-15T23:00:00.000Z'),
		(3, 3, '2035-04-01T20:00:00.000Z'), 
		(3, 3, '2035-04-08T20:00:00.000Z'),
		(3, 3, '2035-04-15T20:00:00.000Z');
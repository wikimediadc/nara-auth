nara-auth
=========

NARA authority files importer for WikiData. Created as part of WikiMedia DC's WikiHack 
meetup at the Sunlight Foundation, 2014-04-05.

When running, specify the root directory to scan for XML files as the first parameter,
and the name of the output file as the second parameter. For example:

	python nara-auth.py data/ output.p
	
The script outputs the data as a list of dictionaries, with each list item corresponding 
to an authority file, and the content of each list item being a Python dictionary (key : 
value pairs), corresponding to the elements and values of the original XML files. The 
output object is dumped as a pickle serialization.


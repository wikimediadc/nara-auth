nara-auth
=========
NARA authority files importer for Wikidata. Created as part of Wikimedia DC's Open Government
WikiHack meetup at the Sunlight Foundation, 5-6 April 2014.


auth-harvest.py
---------------
When running auth-harvest.py, which is designed to harvest data from NARA's organizational 
authority files on Data.gov, specify the root directory to scan for XML files 
as the first parameter, and the name of the output file as the second parameter. For example:

	python auth-harvest.py data/ output.p
	
The script outputs the data as a list of dictionaries, with each list item corresponding 
to an authority file, and the content of each list item being a Python dictionary (key : 
value pairs), corresponding to the elements and values of the original XML. The output 
object is dumped into a pickle serialization under the name passed to the script as the 
second parameter.


wd_interact.py
--------------
To run the wikidata python script, wd_interact.py, use the following commands

```bash
python wd_interact.py search # uses smalllist.p to reference wikidata ids to nara org ids
python wd_interact.py mass_edit # updates the wikidata entries
python wd_interact.py create_ref # creates a reference for a specific claim for a specific wikidata item
```

License
----
CC0

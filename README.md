Metonym galaxy
==============

First part of the project module to populate the meaning of words and their synonyms with meaning and sentences is done. 

##### REQUIREMENTS #####
1. Python modules 
    * CURD.py>=0.4.1
    * Flask
    * urllib2
    * BeautifulSoup4

To install them run 
```
sudo pip intall -r requirements.txt
```
2. MySQL Server
create tables in a mysql database
and edit accordingly
```
populate_dictionary/config.py
```

Create tables with SQL provided in 
```
tables.sql
```
##### START SERVER #####

Edit the port number in runserver.py
```
DEFAULT = 5100
```

To run webserver execute
```
python runserver.py
```

And you are done :-)

Start querying words and get meanings with synonyms 

```
NOTE: Internet is required, if the word is not found in database it searches net and stores result in database
```


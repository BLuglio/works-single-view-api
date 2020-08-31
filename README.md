# works-single-view-api

## Table of Contents

- [Description](#description)
- [Dependencies](#dependencies)
- [Setup](#setup)
- [Usage](#usage)
- [Questions](#questions)

## Description

This is the repository for the second part of the test assigned to me by BMAT. I used `flask` as web server, exposing its api with the `flask-restful` module. The software has to work with the same database used in the first part of the assignment.

Project structure:
```
.
├── README.md
├── app
│   ├── dataaccess
│   │   ├── __init__.py
│   │   ├── db.py
│   ├── download
│   ├── upload
│   ├── util
│   │   ├── __init__.py
│   │   ├── csv.py
│   │   └── processor.py
├── endpoints
│   ├── __init__.py
│   ├── musical_work
│   │   ├── __init__.py
│   │   ├── model.py
│   │   └── resource.py
├── settings.py
├── api.py
├── requirements.txt
└── main.py
```

* endpoints - holds the only endpoint relative to the musical works; `resource.py` contains the logic and data model associated with the http requests, while `model.py` is used to interface with data at db level
* main.py - flask application initialization
* api.py - the API definition
* settings.py - all global app settings
* dataaccess - holds the database management
* util - utility functions; the script inside `processor.py` is the same one that is used in the first part of the assignment plus some basic modifications to integrate it with the current app

## Dependencies

- Python 3.7.7
- Pip >= 19.2.3
- Flask
- Flask-RESTful
- numpy
- pandas
- psycopg2

## Setup

1) Create a virtual environment

``` 
python3 -m venv <env_name> 
``` 

2) Activate it:

``` 
source app/<env_name>/bin/activate 
``` 

3) Install the dependencies in the requirements.txt file:
``` 
pip install -r app/requirements.txt 
``` 

4) Set the configuration in the app/settings.py file

``` 
UPLOAD_FOLDER = '/absolute/path/to/app/upload'
DOWNLOAD_FOLDER = '/absolute/path/to/app/download'
ALLOWED_EXTENSIONS = {'csv'}

DB_HOST = 'db'
DB_PORT = 5432
DB_NAME = 'bmat'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
``` 
Launch it with the command:
``` 
python3 main.py 
``` 

Note that I intentionally serve the app with the development server in order to take advantage of the logging and debugging.

## Usage

#### Musical Works Endpoint

GET http://localhost:5000/api/musical_works

RESPONSE
```javascript
[
    {
        "id": 1,
        "iswc": "T9204649558",
        "url": "http://localhost:5000/api/musical_works/T9204649558"
    },
    {
        "id": 2,
        "iswc": "T0101974597",
        "url": "http://localhost:5000/api/musical_works/T0101974597"
    },
    {
        "id": 3,
        "iswc": "T9214745718",
        "url": "http://localhost:5000/api/musical_works/T9214745718"
    },
    {
        "id": 4,
        "iswc": "T0046951705",
        "url": "http://localhost:5000/api/musical_works/T0046951705"
    }
]
```
GET http://localhost:5000/api/musical_works/T0101974597

RESPONSE
```javascript
{
    "id": 2,
    "iswc": "T0101974597",
       "contributors": [
           "O Brien Edward John",
           "Selway Philip James",
           "Greenwood Colin Charles",
           "Yorke Thomas Edward"
       ],
    "title": "Adventure of a Lifetime",
    "created_at": "2020-08-28 16:52:14",
    "modified_at": "2020-08-28 18:28:10",
    "download": "http://localhost:5000/api/musical_works/T0101974597/download",
    "upload": "http://localhost:5000/api/musical_works/T0101974597/upload"
}
```

GET http://localhost:5000/api/musical_works/T0101974597/download

RESPONSE

![CSV export](github/csv_download.png "Musical Work, Single View")


POST http://localhost:5000/api/musical_works/T0101974597/upload

Example of async request in Javascript with JQuery:
```javascript
var form = new FormData();
form.append("file", "/Users/biagio/Desktop/works_metadata.csv");

var settings = {
  "async": true,
  "crossDomain": true,
  "url": "http://localhost:5000/api/musical_works/T9204649558/upload",
  "method": "POST",
  "processData": false,
  "contentType": false,
  "mimeType": "multipart/form-data",
  "data": form
}

$.ajax(settings).done(function (response) {
  console.log(response);
});
```

RESPONSE

200
```javascript
{
    "message": "File works_metadata.csv uploaded successfully",
    "url": "http://localhost:5000/api/musical_works/T9204649558"
}
```
400 (example):
```javascript
{
    "message": "file not allowed"
}
```
## Questions

1) <b>Imagine that the Single View has 20 million musical works, do you think your solution would have a similar response time?</b>
    <br/>
    I don't have any experience with managing such a huge dataset but I can foresee that, in case of 20 million entries, the response time of my solution will be much slower, especially on the endpoints that perform `SELECT` operations on the database. The unique constraint that I defined on the iswc column could be beneficial since under the hood the postgres engine creates a b-tree index on it, but it couldn't be sufficient to guarantee a fast response

2) <b>If not, what would you do to improve it?</b><br/>
    I would start by testing and evaluating the performance and then I would try for sure some table partitioning strategy for storing the musical works instead of having them all in a single table. The queries' response time could also be improved by adding a caching mechanism (the one provided by the flask framework itself or maybe using an external application like Redis, for example) so that the results already fetched will be retrieved faster. I would also experiment with a text-based search engine like ElasticSearch, connecting it with the db and changing the `get` endpoints logic in order to use the API exposed by the service instead of accessing the db directly
    

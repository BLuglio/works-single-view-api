# works-single-view-api

This is the repository for the second part of the test assigned to me by BMAT.

Once started, the software:

processes every csv file inside the data directory
waits for new csv files created inside the same directory
Further details regarding the file processing are provided in the answers section.

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

RESPONSE: csv file


POST http://localhost:5000/api/musical_works/T0101974597/upload

RESPONSE
```javascript
{
    "message": "File works_metadata.csv uploaded successfully"
}
```
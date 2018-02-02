## Get Table [POST]

Retrieve data from Cassandra table. It takes a few parameters which identify 
the data source `keyspace` and `tablename`. Other optional parameters are aimed to apply DML functionality: `groupby`, `select`, `calculated`, etc.

>Source code
- [javascript](get-table_javascript.md)
- [python](get-table_python.md)
- [java](get-table_java.md)

+ Request (application/json)

```js
        {
            "keyspace": "examples",
            "tablename":"mock_data",
            "filter": "email like \"%am%\"",
            "sortby": [
                {"gender": "asc"},
                {"first_name": "asc"}
            ]
        }
```

+ Response 200 (application/json)

    + Headers

            Location: /get-table

    + Body

```js
            {
                "calculated": null,
                "data": {
                    "birth_date": {
                        "0": "Mon, 24 May 1976 00:00:00 GMT",
                        "1": "Mon, 26 Aug 1963 00:00:00 GMT",
                        "2": "Tue, 20 Jun 1989 00:00:00 GMT",
                        "3": "Fri, 17 Feb 1995 00:00:00 GMT",
                        "4": "Tue, 25 Mar 1980 00:00:00 GMT",
                        "5": "Sat, 03 Jul 1976 00:00:00 GMT",
                        "6": "Sun, 23 May 1993 00:00:00 GMT",
                        "7": "Wed, 09 Jun 1982 00:00:00 GMT",
                        "8": "Sun, 13 Sep 1970 00:00:00 GMT",
                        "9": "Mon, 14 Aug 1978 00:00:00 GMT",
                        "10": "Mon, 23 Dec 1996 00:00:00 GMT",
                        "11": "Sat, 26 Oct 1968 00:00:00 GMT",
                        "12": "Thu, 15 Mar 1984 00:00:00 GMT",
                        "13": "Thu, 19 Jun 1986 00:00:00 GMT",
                        "14": "Sat, 24 Nov 1990 00:00:00 GMT",
                        "15": "Mon, 23 Aug 1982 00:00:00 GMT"
                    },
                    "drinker": {
                        "0": "Yearly",
                        "1": "Seldom",
                        "2": "Often",
                        "3": "Weekly",
                        "4": "Monthly",
                        "5": "Never",
                        "6": "Seldom",
                        "7": "Weekly",
                        "8": "Never",
                        "9": "Often",
                        "10": "Often",
                        "11": "Once",
                        "12": "Weekly",
                        "13": "Weekly",
                        "14": "Daily",
                        "15": "Weekly"
                    },
                    "email": {
                        "0": "apeticang9@examiner.com",
                        "1": "amcilvaneybi@engadget.com",
                        "2": "alaundonev@examiner.com",
                        "3": "atrippickba@amazonaws.com",
                        "4": "amoscropg6@howstuffworks.com",
                        "5": "amcquilty1v@purevolume.com",
                        "6": "aphippardop@acquirethisname.com",
                        "7": "amatejkac4@redcross.org",
                        "8": "abeamsonpu@theatlantic.com",
                        "9": "amcadam8q@dailymail.co.uk",
                        "10": "amaccauleyb0@about.me",
                        "11": "ascampionnw@multiply.com",
                        "12": "bbutchartps@acquirethisname.com",
                        "13": "bfoulghamfn@icio.us",
                        "14": "cstamp1x@arstechnica.com",
                        "15": "cspringhamcf@cnn.com"
                    },
                    "first_name": {
                        "0": "Aeriell",
                        "1": "Ailee",
                        "2": "Alfie",
                        "3": "Alisha",
                        "4": "Alisun",
                        "5": "Alix",
                        "6": "Angelle",
                        "7": "Anna",
                        "8": "Aprilette",
                        "9": "Ardisj",
                        "10": "Asia",
                        "11": "Atalanta",
                        "12": "Benedikta",
                        "13": "Blondelle",
                        "14": "Cal",
                        "15": "Carrissa"
                    },
                    "gender": {
                        "0": "Female",
                        "1": "Female",
                        "2": "Female",
                        "3": "Female",
                        "4": "Female",
                        "5": "Female",
                        "6": "Female",
                        "7": "Female",
                        "8": "Female",
                        "9": "Female",
                        "10": "Female",
                        "11": "Female",
                        "12": "Female",
                        "13": "Female",
                        "14": "Female",
                        "15": "Female"
                    },
                    "id": {
                        "0": 1585,
                        "1": 1414,
                        "2": 1535,
                        "3": 1406,
                        "4": 1582,
                        "5": 1067,
                        "6": 1889,
                        "7": 1436,
                        "8": 1930,
                        "9": 314,
                        "10": 1396,
                        "11": 1860,
                        "12": 928,
                        "13": 563,
                        "14": 1069,
                        "15": 447
                    },
                    "image": {
                        "0": "http://dummyimage.com/174x241.bmp/ff4444/ffffff",
                        "1": "http://dummyimage.com/185x150.jpg/cc0000/ffffff",
                        "2": "http://dummyimage.com/191x218.bmp/cc0000/ffffff",
                        "3": "http://dummyimage.com/239x241.bmp/ff4444/ffffff",
                        "4": "http://dummyimage.com/229x149.jpg/dddddd/000000",
                        "5": "http://dummyimage.com/196x103.jpg/dddddd/000000",
                        "6": "http://dummyimage.com/169x110.png/cc0000/ffffff",
                        "7": "http://dummyimage.com/189x137.png/dddddd/000000",
                        "8": "http://dummyimage.com/150x163.png/cc0000/ffffff",
                        "9": "http://dummyimage.com/176x229.bmp/ff4444/ffffff",
                        "10": "http://dummyimage.com/216x136.png/cc0000/ffffff",
                        "11": "http://dummyimage.com/151x211.png/5fa2dd/ffffff",
                        "12": "http://dummyimage.com/202x118.bmp/5fa2dd/ffffff",
                        "13": "http://dummyimage.com/128x146.png/dddddd/000000",
                        "14": "http://dummyimage.com/246x210.png/ff4444/ffffff",
                        "15": "http://dummyimage.com/139x188.bmp/5fa2dd/ffffff",
                        ...
                    },
                    "ip_address": {
                        "0": "74.27.65.10",
                        "1": "150.169.167.205",
                        "2": "11.97.180.107",
                        "3": "23.62.181.188",
                        "4": "201.173.152.217",
                        "5": "89.31.254.214",
                        "6": "226.204.241.133",
                        "7": "96.236.158.209",
                        "8": "108.120.238.132",
                        "9": "212.124.145.38",
                        "10": "171.18.144.210",
                        "11": "0.86.156.233",
                        "12": "68.91.49.20",
                        "13": "26.37.223.153",
                        "14": "37.168.113.214",
                        "15": "167.44.129.204"
                    },
                    "language": {
                        "0": "Tsonga",
                        "1": "Kurdish",
                        "2": "Telugu",
                        "3": "English",
                        "4": "Burmese",
                        "5": "Bengali",
                        "6": "Catalan",
                        "7": "Tamil",
                        "8": "Maltese",
                        "9": "Tswana",
                        "10": "Quechua",
                        "11": "Azeri",
                        "12": "Estonian",
                        "13": "Gagauz",
                        "14": "Montenegrin",
                        "15": "Tetum"
                    },
                    "last_name": {
                        "0": "Petican",
                        "1": "McIlvaney",
                        "2": "Laundon",
                        "3": "Trippick",
                        "4": "Moscrop",
                        "5": "McQuilty",
                        "6": "Phippard",
                        "7": "Matejka",
                        "8": "Beamson",
                        "9": "McAdam",
                        "10": "MacCauley",
                        "11": "Scampion",
                        "12": "Butchart",
                        "13": "Foulgham",
                        "14": "Stamp",
                        "15": "Springham"
                    },
                    "probability": {
                        "0": 1.0,
                        "1": 0.0,
                        "2": 0.0,
                        "3": 1.0,
                        "4": 0.0,
                        "5": 0.0,
                        "6": 0.0,
                        "7": 1.0,
                        "8": 0.0,
                        "9": 1.0,
                        "10": 1.0,
                        "11": 1.0,
                        "12": 1.0,
                        "13": 0.0,
                        "14": 0.0,
                        "15": 1.0
                    },
                    "smoker_bool": {
                        "0": false,
                        "1": true,
                        "2": false,
                        "3": false,
                        "4": true,
                        "5": false,
                        "6": false,
                        "7": true,
                        "8": false,
                        "9": true,
                        "10": true,
                        "11": false,
                        "12": true,
                        "13": true,
                        "14": false,
                        "15": false
                    }
                },
                "groupby": null,
                "join_key": [],
                "keyspace": "examples",
                "s_filter": "email like \"%am%\"",
                "save": null,
                "select": null,
                "sortby": [
                    {
                        "gender": "asc"
                    },
                    {
                        "first_name": "asc"
                    }
                ],
                "status": 200,
                "success": true,
                "tablename": "mock_data"
}
```


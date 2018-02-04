```javascript
var settings = {
  "async": true,
  "crossDomain": true,
  "url": "http://localhost:5000/get-table",
  "method": "POST",
  "headers": {
    "content-type": "application/json"
  },
  "processData": false,
  "data": "{\n\t\"keyspace\": \"examples\",\n\t\"tablename\":\"mock_data\",\n\t\"filter\": \"email like \\\"%am%\\\"\",\n\t\"sortby\": [\n\t\t{\"gender\": \"asc\"},\n\t\t{\"first_name\": \"asc\"}\n\t]\n}"
}

$.ajax(settings).done(function (response) {
  console.log(response);
});
```

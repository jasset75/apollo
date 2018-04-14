## Union [/union]

### Union [POST]

It makes a union between two members, both could be a table, join or union, evaluated in a recursive way. It takes a few parameters which identify 
the data source `keyspace` and `tablename`. Other optional parameters are aimed to apply DML functionality: `groupby`, `select`, `calculated`, etc.

- left operand: table description, join description or union description
- right operand: table description, join description or union description

|   | Possible combinations|   |
|:--|:--:|:--|
| table_a  |&#8746;|  table_b |
| table_a  |&#8746;|  join_b  |
| table_a  |&#8746;|  union_b |
| join_a   |&#8746;|  table_b |
| join_a   |&#8746;|  join_b  |
| join_a   |&#8746;|  union_b |
| union_a  |&#8746;|  table_b |
| union_a  |&#8746;|  join_b  |
| union_a  |&#8746;|  union_b |

- Select

    Projection operation of relational algebra. It allows rename operation as well.

    ```javascript
    "select": [<field_a>, <field_b>, {<field_c>: <field_c_renamed>}, ... ],
    ```

- Calculated

    Optional parameter that allows Spark SQL expressions which calculate new fields from others.

    ```javascript
    "calculated": {
        <calculated_field>: <Spark SQL expression>
    },
    ```

- Filter

    Filter expression

    ```javascript
    "filter": <filter_expression>,
    ```

- Group by

    Apply a `groupby` statement over two members grouped. 

    ```javascript
    "groupby": { 
        "grouped": [<field_a>],
        "agg": {
            "count": [<field_b>]
        }
    }
    ```

- Sort by
    
    ```javascript
    "sortby": [
        {<field_a>: "desc"},
        {<field_b>: "asc"},  //default
        ...
    ]
    ```

- Save

    It writes back results into Cassandra existing table. The result set must be compatible with Cassandra table structure but as flexible as Cassandra is.

    ```javascript
    "save": {
        "keyspace": <destination keyspace>,
        "tablename": <destination table>
    }
    ```

- Shell snippet

```sh
curl --request POST \
    --url http://localhost:5000/union \
    --header 'content-type: application/json' \
    --data '  {
        "table_a": {
            "keyspace": "examples",
            "tablename": "mock_cars",
            "select": [],
            "filter": "color == \"Blue\""
        },
        "table_b": {
            "keyspace": "examples",
            "tablename": "mock_cars",
            "select": [],
            "filter": "color == \"Red\""
        }
    }'
```

```javascript
// Response 200 OK
{
    "calculated": null,
    "data": {
        "car_id": {
            "0": "f52a0f09-0e2d-46b6-b79c-588305afb489",
            "1": "33b07a75-2507-4d14-923c-87f8c17e034b",
            "2": "70e289f2-935a-4ea7-a4a3-eaa8f2c8ac9b",
            "3": "78a5c5bb-89e9-4922-b3a7-3d1444aa0261",
            "4": "e6e6a3d4-3283-4adc-ad19-bb00c2d48495",
            "5": "d262a903-a259-4533-994c-7f92bd3c53b3",
            "6": "a41a2ca1-0a95-470f-aaf7-847cdfe8d828",
            "7": "ea355147-0401-4572-b881-b139b8ff6327",
            "8": "5acf6fde-56ca-4cd5-b76c-68997081fa2d",
            "9": "7150b2f9-5bac-4b27-b5f4-33828bf21253",
            "10": "a41e2d2b-404e-4fb9-aff6-1aa65cd85491",
            ...

            "47": "1a8c51d5-a4fb-4f9f-946e-8ab5b0add613",
            "48": "e9ffa861-4773-4bc8-865e-bc8a7436cef6",
            "49": "86b69f88-2577-4edc-a227-66744ebf3418",
            "50": "6025fff5-b649-460c-b55f-3d0d4e449655",
            "51": "a94deef3-4185-4cc6-83ab-624c0993e6ca",
            "52": "01feb5e1-6b27-4972-b828-b94ddcc55926",
            "53": "ea42bc1e-1f55-44cb-b213-ab2af3d582a1",
            "54": "e20d1c0e-ad68-4f99-a78e-404511b4a4bb",
            "55": "41f8ffae-3de7-41b5-9bb3-1744d7e07d8b",
            "56": "4e1c886a-3187-4183-9fe1-83b7bddbdbe3",
            "57": "366a369c-b6ae-4e2d-a94e-c92c14f45b20",
            ...
        },
        "car_make": {
            "0": "Ferrari",
            "1": "Acura",
            "2": "GMC",
            "3": "Mercedes-Benz",
            "4": "Subaru",
            "5": "Lexus",
            "6": "Chevrolet",
            "7": "Hyundai",
            "8": "Honda",
            "9": "Pontiac",
            "10": "Maybach",
            ...

            "47": "Mercury",
            "48": "Kia",
            "49": "Chevrolet",
            "50": "Saturn",
            "51": "Audi",
            "52": "Ford",
            "53": "Mitsubishi",
            "54": "Chevrolet",
            "55": "Toyota",
            "56": "Honda",
            "57": "Chevrolet",
            ...
        },
        "car_model": {
            "0": "612 Scaglietti",
            "1": "NSX",
            "2": "Sonoma",
            "3": "G-Class",
            "4": "Forester",
            "5": "LS Hybrid",
            "6": "Avalanche 1500",
            "7": "Elantra",
            "8": "S2000",
            "9": "Safari",
            "10": "57S",
            ...

            "47": "Mountaineer",
            "48": "Sportage",
            "49": "Astro",
            "50": "Ion",
            "51": "Allroad",
            "52": "E350",
            "53": "Lancer Evolution",
            "54": "Silverado 3500",
            "55": "RAV4",
            "56": "Prelude",
            "57": "Equinox",
            ...
        },
        "car_model_year": {
            "0": 2006,
            "1": 1996,
            "2": 1992,
            "3": 2006,
            "4": 2007,
            "5": 2010,
            "6": 2005,
            "7": 2003,
            "8": 2005,
            "9": 1989,
            "10": 2005,
            ...

            "47": 2003,
            "48": 1998,
            "49": 2002,
            "50": 2003,
            "51": 2001,
            "52": 2004,
            "53": 2003,
            "54": 2010,
            "55": 2012,
            "56": 1994,
            "57": 2005,
            ...
        },
        "color": {
            "0": "Blue",
            "1": "Blue",
            "2": "Blue",
            "3": "Blue",
            "4": "Blue",
            "5": "Blue",
            "6": "Blue",
            "7": "Blue",
            "8": "Blue",
            "9": "Blue",
            "10": "Blue",
            ...

            "47": "Red",
            "48": "Red",
            "49": "Red",
            "50": "Red",
            "51": "Red",
            "52": "Red",
            "53": "Red",
            "54": "Red",
            "55": "Red",
            "56": "Red",
            "57": "Red",
            ...
        },
        "id_owner": {
            "0": 52,
            "1": 128,
            "2": 803,
            "3": 241,
            "4": 76,
            "5": 858,
            "6": 486,
            "7": 145,
            "8": 42,
            "9": 877,
            "10": 724,
            ...
            "47": 223,
            "48": 641,
            "49": 450,
            "50": 231,
            "51": 640,
            "52": 624,
            "53": 888,
            "54": 674,
            "55": 578,
            "56": 200,
            "57": 182,
            ...
        },
        "registration": {
            "0": "3104-ELC",
            "1": "2505-PIM",
            "2": "9636-FLX",
            "3": "5263-DQS",
            "4": "5382-OQM",
            "5": "1157-BJE",
            "6": "7514-YCT",
            "7": "7590-NTT",
            "8": "0189-BMC",
            "9": "8365-NSW",
            "10": "4643-MJO",
            ...

            "46": "6817-SYC",
            "47": "3071-PDH",
            "48": "9307-YLU",
            "49": "2691-RBI",
            "50": "7224-BCG",
            "51": "1279-NNT",
            "52": "4107-TZV",
            "53": "1138-SMC",
            "54": "0392-VLM",
            "55": "3629-GFQ",
            "56": "6365-HYN",
            "57": "7891-QWU",
        }
    },
    "join_a": null,
    "join_b": null,
    "join_key": [],
    "s_filter": null,
    "save": null,
    "select": null,
    "sortby": null,
    "status": 200,
    "success": true,
    "table_a": {
        "filter": "color == \"Blue\"",
        "keyspace": "examples",
        "select": [],
        "tablename": "mock_cars"
    },
    "table_b": {
        "filter": "color == \"Red\"",
        "keyspace": "examples",
        "select": [],
        "tablename": "mock_cars"
    },
    "union_a": null,
    "union_b": null,
    "union_groupby": null,
    "union_type": "union_all"
}
```

```sh
curl --request POST \
    --url http://localhost:5000/union \
    --header 'content-type: application/json' \
    --data '  {
        "table_a": {
            "keyspace": "examples",
            "tablename": "mock_cars",
            "select": [],
            "filter": "color == \"Blue\""
        },
        "union_b": {
            "table_a": {
                    "keyspace": "examples",
                    "tablename": "mock_cars",
                    "select": [],
                    "filter": "color == \"Red\""
            },          
            "table_b": {
                    "keyspace": "examples",
                    "tablename": "mock_cars",
                    "select": [],
                    "filter": "color == \"Yellow\""
            }           
        }
    }'
```

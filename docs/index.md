# Apollo Microservice v1.0 Alpha

This project implements a REST API to select data from Apache Cassandra taking advantage of the power of Apache Spark. Spark cluster computes commands requested by HTTP client through Apollo API endpoints.

I've written this [notes](https://jasset75.github.io/Spark-Cassandra-Notes/Environment.html) with which to follow a recipe to build a development environment. Besides, there are some examples and scripts which loads the data sources used in those and these examples.

> API Blueprint format.
> NOTE: The data for examples and test are based on [Spark-Cassandra Notes repository](https://jasset75.github.io/Spark-Cassandra-Notes/).

# Apollo REST API

Spark-Cassandra Rest API

Apollo is a Microservice which allows data computing with Apache Spark from Apache Cassandra database.

Apache Cassandra is a highly scalable platform, it is ready to store a huge volume 
of data but it is not able to do join between data tables, 
so in order to make this kind of algebraic operations we need a tool like Apache Spark, powerful and highly scalable as well.

This API implements an interface between an app client and Spark-Cassandra environment. Furthermore, using Sparl SQL module we access to join, union... relational algebra operations in general.

## About [/about]

### About [GET]

Gets detail about authorship, version number, documentation, etc.

+ Response 200 (application/json)

        {
            "api_name": "Apollo",
            "author_email": "juanantonioaguilar@gmail.com",
            "author_name": "Juan A. Aguilar-Jiménez",
            "documentation": "http://jasset75.github.io/apollo",
            "license": "Apache 2.0",
            "project_repository": "https://github.com/jasset75/apollo.github",
            "version": 1.0
        }

## Version [/version]

### Version [GET]

Gets version information.

+ Response 200 (application/json)

        {
            "api_name": "Apollo",
            "license": "Apache 2.0",
            "status": 200,
            "version": 1.0
        }


## Create Table [/create-table]

### Create Table [POST]

Creates Cassandra Table.

Accepted parameters:


- keyspace

    Cassandra keyspace where the table will lay. Created if not exists.

- tablename

    Cassandra table name to be created. 

- columns

    JSON list of objects defining table's columns to be created. Each columns has these own properties:


- db_field

    The fieldname this field will map to in the database

- db_type 

    Column type correspondig to Cassandra column types:
    
    - Ascii

        Stores a US-ASCII character string

    - BigInt

        Stores a 64-bit signed long value

    - Blob

        Stores a raw binary value

    - Bytes

        alias of Blob

    - Boolean

        Stores a boolean True or False value

    - Counter

        Stores a counter that can be inremented and decremented

    - Date

        Note: this type is overloaded, and will likely be changed or removed to accommodate distinct date type in a future version

        Stores a date value, with no time-of-day

    - DateTime

        Stores a datetime value

    - Decimal

        Stores a variable precision decimal value

    - Float

        double_precision

        Stores a floating point value

    - Integer

        Stores a 32-bit signed integer value

    - List

        Stores a list of ordered values

        [Datastax documentation about use of lists](http://www.datastax.com/documentation/cql/3.1/cql/cql_using/use_list_t.html)
       
        > Parameters: value_type – a column class indicating the types of the value

    - Map

        Stores a key -> value map (dictionary)

        [Datastax documentation about use of map column type](http://www.datastax.com/documentation/cql/3.1/cql/cql_using/use_map_t.html)

        > Parameters: 

        >    key_type – a column class indicating the types of the key
        >    value_type – a column class indicating the types of the value

    - Set

        Stores a set of unordered, unique values

        [Datastax documentation about use of set column type](http://www.datastax.com/documentation/cql/3.1/cql/cql_using/use_set_t.html)
       
        > Parameters: 

        >    value_type – a column class indicating the types of the value
        >    strict – sets whether non set values will be coerced to set type on validation, or raise a validation error, defaults to True

    - Text

        Stores a UTF-8 encoded string

        > Parameters: 

        >    min_length (int) – Sets the minimum length of this string, for validation purposes. Defaults to 1 if this is a required column. Otherwise, None.
        >    max_lemgth (int) – Sets the maximum length of this string, for validation purposes.

    - TimeUUID

        UUID containing timestamp

    - UUID

        Stores a type 1 or 4 UUID

    - VarInt

        Stores an arbitrary-precision integer


- *value_type*:

    Some types (i.e.: map, list, set) are complex types which needs to define value type within the collection

- *primary_key*  = False

    bool flag, indicates this column is a primary key. The first primary key defined on a model is the partition key (unless partition keys are set), all others are cluster keys

- partition_key = False

    indicates that this column should be the partition key, defining more than one partition key column creates a compound partition key

- index = False

    bool flag, indicates an index should be created for this column


- default = None

    the default value, can be a value or a callable (no args)

- required = False

    boolean, is the field required? Model validation will raise and exception if required is set to True and there is a None value assigned

- clustering_order = None

    only applicable on clustering keys (primary keys that are not partition keys) determines the order that the clustering keys are sorted on disk

- discriminator_column = False

    boolean, if set to True, this column will be used for discriminating records of inherited models.

    Should only be set on a column of an abstract model being used for inheritance.

    There may only be one discriminator column per model. See __discriminator_value__ for how to specify the value of this column on specialized models.

- static = False

    boolean, if set to True, this is a static column, with a single value per partition

Reference [Datastax](https://docs.datastax.com/en/drivers/python/2.5/api/cassandra/cqlengine/columns.html)

Shell snippets

    - Simple types

        ```sh
            curl --request POST \
              --url http://localhost:5000/create-table \
              --header 'content-type: application/json' \
              --data '{
                "keyspace": "examples_bis",
                "tablename": "older_than_40_summarized",
                "columns": [
                    {
                        "db_field": "age",
                        "db_type": "integer",
                        "primary_key": "true"
                    }, 
                    {
                        "db_field": "total",
                        "db_type": "Integer" 
                    }
                ]
            }'
        ```

        > Response
        ```javascript
            // Response 201 OK
            {
                "success": true,
                "data": null,
                "columns": [
                    {
                        "db_field": "age",
                        "db_type": "integer",
                        "primary_key": "true"
                    },
                    {
                        "db_field": "total",
                        "db_type": "Integer"
                    }
                ],
                "status": 201,
                "tablename": "older_than_40_summarized",
                "keyspace": "examples_bis"
            }
        ```

    - Table with counter field

        ```sh
            curl --request POST \
              --url http://localhost:5000/create-table \
              --header 'content-type: application/json' \
              --data '{
                "keyspace": "examples",
                "tablename": "test_2",
                "columns": [
                    {
                        "db_field": "field_1",
                        "db_type": "uuid",
                        "primary_key": "true"
                    },
                    {
                        "db_field": "field_2",
                        "db_type": "counter"
                    }
                ]
            }'    
        ```

        > Response
            {
                // Response 201 OK
                "tablename": "test",
                "status": 201,
                "success": true,
                "keyspace": "examples",
                "data": null,
                "columns": [
                    {
                        "db_type": "text",
                        "db_field": "field_1"
                    },
                    {
                        "db_type": "integer",
                        "db_field": "field_2",
                        "primary_key": "true"
                    }
                ]
            }

## Get Table [/get-table]

### Get Table [POST]

Retrieve data from Cassandra table. It takes a few parameters which identify 
the data source `keyspace` and `tablename`. Other optional parameters are aimed to apply DML functionality: `groupby`, `select`, `calculated`, etc.

- Select

    Projection operation of relational algebra. It allows rename operation as well.


    ```javascript
        "select": [<field_a>, <field_b>, {<field_c>: <field_c_renamed>}, ... ],
    ```
- Calculated

    Optional parameter that allow Spark SQL expressions which calculate new fields from others.

    ```javascript
        "calculated": {
            "<calculated_field": "<Spark SQL expression"
        },
    ```

- Filter

    Filter expression

    ```javascript
        "filter": <filter_expression>,
    ```

- Group by

    Gets data from Cassandra table which is applied a `groupby` statement. 

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

> Test Details
> People from mock_data table who is older than 40 years old and grouped by age with count aggregation.
> Age is calculated from `birth_date` field, indicated by `calculated` clause.

Shell snippet

```sh
    curl --request POST \
      --url http://localhost:5000/get-table \
      --header 'content-type: application/json' \
      --data '{
        "keyspace": "examples",
        "tablename":"mock_data",
        "calculated": {
            "age": "round(months_between(current_date(),birth_date)/12,0)"
        },
        "filter": "age > 40",
        "groupby": { 
            "grouped": ["age"],
            "agg": {
                "count": [{"id": "total"}]
            }
        },
        "sortby": [{"total": "desc"}],
        "save": {
            "keyspace": "examples_bis",
            "tablename": "older_than_40_summarized"
        }
    }'
```

```javascript
    // Response 200 OK
    {
        "calculated": {
            "age": "round(months_between(current_date(),birth_date)/12,0)"
        },
        "data": {
            "age": {
                "0": 51.0,
                "1": 48.0,
                "2": 61.0,
                "3": 63.0,
                "4": 62.0,
                "5": 55.0,
                "6": 57.0,
                "7": 41.0,
                "8": 49.0,
                "9": 42.0,
                "10": 47.0,
                "11": 44.0,
                "12": 52.0,
                "13": 54.0,
                "14": 56.0,
                "15": 58.0,
                "16": 45.0,
                "17": 46.0,
                "18": 43.0,
                "19": 50.0,
                "20": 59.0,
                "21": 53.0,
                "22": 60.0
            },
            "count(id)": {
                "0": 56,
                "1": 56,
                "2": 54,
                "3": 53,
                "4": 52,
                "5": 50,
                "6": 49,
                "7": 48,
                "8": 47,
                "9": 47,
                "10": 46,
                "11": 43,
                "12": 43,
                "13": 43,
                "14": 42,
                "15": 42,
                "16": 39,
                "17": 39,
                "18": 38,
                "19": 37,
                "20": 37,
                "21": 36,
                "22": 32
            }
        },
        "groupby": {
            "agg": {
                "count": [
                    "id"
                ]
            },
            "grouped": [
                "age"
            ]
        },
        "join_key": [],
        "keyspace": "examples",
        "s_filter": "age > 40",
        "save": null,
        "select": null,
        "sortby": [
            {
                "count(id)": "desc"
            }
        ],
        "status": 200,
        "success": true,
        "tablename": "mock_data"
    }
```

## Join [/join]

### Join [POST]

Retrieve data from two Cassandra data sets and join them by key fields. It accepts two kind of parameters: simple table description that is an operand; or an operation, two choices also: recursive join description or a recursive union description, which both are composed of two parameters: 

- left operand: table description, join description or union description
- right operand: table description, join description or union description

Possible combinations:

- table_a |X| table_b
- table_a |X| join_b
- table_a |X| union_b
- join_a |X| table_b
- join_a |X| join_b
- join_a |X| union_b
- union_a |X| table_b
- union_a |X| join_b
- union_a |X| union_b

Thus, recursivelly we could define whatever table merging. Similar to SQL but only binary operations, same functionality.

This descriptions has a few parameters which identify the data source: `keyspace` and `tablename`. Beside this, two descriptions involved in a join operation needs join_key parameter that declare which fields are the key to join each other.

Other optional parameters are aimed to apply DML functionality: `groupby`, `select`, `calculated`, etc.:


- Select

    Projection operation of relational algebra. It allows rename operation as well.


    ```javascript
        "select": [<field_a>, <field_b>, {<field_c>: <field_c_renamed>}, ... ],
    ```
- Calculated

    Optional parameter that allow Spark SQL expressions which calculate new fields from others.

    ```javascript
        "calculated": {
            "<calculated_field": "<Spark SQL expression"
        },
    ```

- Filter

    Filter expression

    ```javascript
        "filter": <filter_expression>,
    ```

- Group by

    Gets data from Cassandra table which is applied a `groupby` statement. 

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

> Test Details
> Ordered list of countries with more than 10K billion Euros of drug annual budget. It summarizes Drug Companies annual budget grouped by country.


Shell snippet

```sh
curl --request POST \
  --url http://localhost:5000/join \
  --header 'content-type: application/json' \
  --data '{
    "join_a": {
        "table_a": {
            "keyspace": "examples",
            "tablename": "mock_data",
            "join_key": [{"id": "id_person"}],
            "calculated": {
                "edad": "round(months_between(current_date(),birth_date)/12,0)"
            },
            "select": ["first_name","last_name","email","gender","drinker","smoker_bool","language","edad"]
        },
        "table_b": {
            "keyspace": "examples_bis",
            "tablename": "mock_drugs",
            "join_key": ["id_patient"],
            "select": ["drug_name","id_company"]
        },
        "join_key": ["id_company"]
    },
    "table_b": {
        "keyspace": "examples_bis",
        "tablename": "mock_companies",
        "join_key": ["id_company"],
        "select": ["annual_budget","city","company_name","country",{"id": "id_company"}]
    },
    "filter": "annual_budget > 10000000000",    
    "groupby": { 
        "grouped": ["country"],
        "agg": {
            "sum": ["annual_budget"]
        }
    },
    "sortby": [
        {"sum(annual_budget)": "desc"}
    ]   
}
```

```javascript
    // Response 200 OK

        {
            "calculated": null,
            "data": {
                "country": {
                    "0": "China",
                    "1": "France",
                    "2": "Poland",
                    "3": "Portugal",
                    "4": "Japan",
                    "5": "Mexico",
                    "6": "Sweden",
                    "7": "United States",
                    "8": "Canada",
                    "9": "Ukraine",
                    "10": "Georgia",
                    "11": "Germany",
                    "12": "Spain",
                    "13": "Norway",
                    "14": "Ireland",
                    "15": "Netherlands"
                },
                "sum(annual_budget)": {
                    "0": 3901666527232.0,
                    "1": 924393641984.0,
                    "2": 706987144192.0,
                    "3": 606915214336.0,
                    "4": 511156410368.0,
                    "5": 507268958208.0,
                    "6": 398938326016.0,
                    "7": 339608810496.0,
                    "8": 283575956480.0,
                    "9": 238798228480.0,
                    "10": 218540765184.0,
                    "11": 166788163584.0,
                    "12": 147850549248.0,
                    "13": 123179765760.0,
                    "14": 111000954880.0,
                    "15": 100029864960.0
                }
            },
            "format": "dict",
            "join_a": {
                "join_key": [
                    "id_company"
                ],
                "table_a": {
                    "calculated": {
                        "edad": "round(months_between(current_date(),birth_date)/12,0)"
                    },
                    "join_key": [
                        {
                            "id": "id_person"
                        }
                    ],
                    "keyspace": "examples",
                    "select": [
                        "first_name",
                        "last_name",
                        "email",
                        "gender",
                        "drinker",
                        "smoker_bool",
                        "language",
                        "edad",
                        {
                            "id": "id_person"
                        }
                    ],
                    "tablename": "mock_data"
                },
                "table_b": {
                    "join_key": [
                        "id_patient"
                    ],
                    "keyspace": "examples_bis",
                    "select": [
                        "drug_name",
                        "id_company",
                        "id_patient"
                    ],
                    "tablename": "mock_drugs"
                }
            },
            "join_b": null,
            "join_groupby": {
                "agg": {
                    "sum": [
                        "annual_budget"
                    ]
                },
                "grouped": [
                    "country"
                ]
            },
            "join_key": [],
            "join_type": "inner",
            "orient_results": "column",
            "s_filter": "annual_budget > 10000000000",
            "save": null,
            "select": null,
            "sortby": [
                {
                    "sum(annual_budget)": "desc"
                }
            ],
            "status": 200,
            "success": true,
            "table_a": null,
            "table_b": {
                "join_key": [
                    "id_company"
                ],
                "keyspace": "examples_bis",
                "select": [
                    "annual_budget",
                    "city",
                    "company_name",
                    "country",
                    {
                        "id": "id_company"
                    }
                ],
                "tablename": "mock_companies"
            },
            "union_a": null,
            "union_b": null
        }
```

## Union [/union]

### Union [POST]

It makes a union between two members, both could be a table, join or union, evaluated in a recursive way. It takes a few parameters which identify 
the data source `keyspace` and `tablename`. Other optional parameters are aimed to apply DML functionality: `groupby`, `select`, `calculated`, etc.

- left operand: table description, join description or union description
- right operand: table description, join description or union description

Possible combinations:

- table_a U table_b
- table_a U join_b
- table_a U union_b
- join_a U table_b
- join_a U join_b
- join_a U union_b
- union_a U table_b
- union_a U join_b
- union_a U union_b

- Select

    Projection operation of relational algebra. It allows rename operation as well.


    ```javascript
        "select": [<field_a>, <field_b>, {<field_c>: <field_c_renamed>}, ... ],
    ```
- Calculated

    Optional parameter that allow Spark SQL expressions which calculate new fields from others.

    ```javascript
        "calculated": {
            "<calculated_field": "<Spark SQL expression"
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

Shell snippet

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


>Updated Source at:
>[Apiary Documentation](https://apollo20.docs.apiary.io)

## Useful tools

### Apiari.io

It is oriented to describe and test REST APIs. Supports Swagger and API Blueprint formats, as well as automation. Integrates with Dredd, which is a framework for validating API description document against backend implementation of the API.

### Insomnia

Insomnia is that kind of applications that is highly recommended to develop a REST API. It has as prominent features:

- Usable GUI
- Different Environment management
- The whole range of HTTP verbs: GET, PUT, POST, DELETE, etc.
- Exportable environment file with JSON format for sharing
- Response beautifier
...

```sh
# Add to sources
echo "deb https://dl.bintray.com/getinsomnia/Insomnia /" \
    | sudo tee -a /etc/apt/sources.list.d/insomnia.list

# Add public key used to verify code signature
wget --quiet -O - https://insomnia.rest/keys/debian-public.key.asc \
    | sudo apt-key add -

# Refresh repository sources and install Insomnia
sudo apt-get update
sudo apt-get install insomnia
```

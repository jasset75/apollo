# Apollo Microservice v1.0 Alpha

This project implements a REST API to select data from Apache Cassandra taking advantage of the power of Apache Spark. Spark cluster computes commands requested by HTTP client through Apollo API endpoints.

I've wrote this [notes](https://jasset75.github.io/Spark-Cassandra-Notes/Environment.html) with which to follow a recipe and mount a development environment. Besides, there are some examples and scripts which loads the data sources used in those and these examples.

> API Blueprint format.
> NOTE: The data for examples and test are based on [Spark-Cassandra Notes repository](https://jasset75.github.io/Spark-Cassandra-Notes/).

## Apollo REST API

# Apollo

Spark-Cassandra Rest API

Apollo is a Microservice which allows data computing with Apache Spark from Apache Cassandra database.

Apache Cassandra is a highly scalable platform, it is ready to store a huge volume 
of data but it is not able to do join between data tables, 
so in order to make this kind of algebraic operations we need a tool like Apache Spark, powerful and highly scalable as well.

This API implements an interface between an app client and Spark-Cassandra environment. Furthermore,
using Sparl SQL module we access to join, union,

## About [/about]

### About [GET]

Gets detail about authorship, version number, documentation, etc.


```javascript
    // response 200 OK
    {
        "api_name": "Apollo",
        "author_email": "juanantonioaguilar@gmail.com",
        "author_name": "Juan A. Aguilar-Jiménez",
        "documentation": "http://jasset75.github.io/apollo",
        "license": "Apache 2.0",
        "project_repository": "https://github.com/jasset75/apollo.github",
        "version": 1.0
    }
```

## Version [/version]

### Version [GET]

Gets version information.

+ Response 200 (application/json)

```javascript
    // response 200 OK
    {
        "api_name": "Apollo",
        "license": "Apache 2.0",
        "status": 200,
        "version": 1.0
    }
```


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
    
- Filter

    Filter expression

    ```javascript
        "filter": <filter_expression>,
    ```

- Group by

    Gets data from Cassandra table which is applied a `groupby` statement. 

    ```javascript
        "groupby": { 
            "grouped": [<field_name_1>],
            "agg": {
                "count": [<field_name_2>]
            }
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

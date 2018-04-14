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

    indicates that this column should be the partition key, defining more than one partition key column creates a compound partition key.

- index = False

    bool flag, indicates an index should be created for this column.

- default = None

    the default value, can be a value or a callable (no args).

- required = False

    boolean, is the field required? Model validation will raise and exception if required is set to True and there is a None value assigned.

- clustering_order = None

    only applicable on clustering keys (primary keys that are not partition keys) determines the order that the clustering keys are sorted on disk.

- discriminator_column = False

    boolean, if set to True, this column will be used for discriminating records of inherited models.

    Should only be set on a column of an abstract model being used for inheritance.

    There may only be one discriminator column per model. See __discriminator_value__ for how to specify the value of this column on specialized models.

- static = False

    boolean, if set to True, this is a static column, with a single value per partition.

Reference [Datastax](https://docs.datastax.com/en/drivers/python/2.5/api/cassandra/cqlengine/columns.html).

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
```javascript
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
```

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

- Stacked

    This is a so specific statement. It's intended for column oriented data source; in other words,
    we need to join two rows with undefined number of values 
    associated to (undefined number of columns), and it is required
    select all values. Thus, we need transponse data-columns to data-rows before select them. To do so,
    it is added a new field `rowid` to identify values of the "same row". 
    Additionally, in a `single-value` strategy we need another component of primary key
    which identify linked values.
    
    Example of data source:

    |key|num|column1|column2|column3|
    |---|---|---|---|---|
    |firstName|1|Picasso|Rodin|Velazquez|
    |firstName|2|Pablo|Auguste|Diego|
    
    Example of configuration:
    
    ```javascript
    "stacked": {
        "auto": false,
        "strategy": "double-value",
        "stack_p_key": ["key"],
        "stack_c_key": ["num"],
        "stack_pair": "rowid",
        "stack_column": "value",
        "filter_field": "num",
        "filter_left_value": 1,
        "filter_right_value": 2
    }
    ```
    
    Fields explained:
        
    - `auto`, when `false` `stack_p_key` is mandatory. `stack_c_key` is needed
    only for `"strategy": "single-value"`.

    - `strategy`, two strategies are possible:
    
        - `single-value`: the data values are transformed from columns to rows, and to identify related values in the same row of the original table, a rowid field with a unique value is added, e.g. UUID.
        
        | key | rowid | num | value |
        |---|---|---|---|
        | firstName |544ca336-2d9c-36bb-8433-17371498d2fe | 1 | Picasso |
        | firstName |544ca336-2d9c-36bb-8433-17371498d2fe | 2 | Pablo |
        | firstName |f1c25492-21b1-314a-8218-75da2d4e8fbd | 1 | Rodin |
        | firstName |f1c25492-21b1-314a-8218-75da2d4e8fbd | 2 | Auguste |
        | firstName |f1c25492-21b1-314a-8218-1608134e5815 | 1 | Velazquez |
        | firstName |f1c25492-21b1-314a-8218-1608134e5815 | 2 | Diego |
        
        - `double-value`: to associate the two data values that form a pair, each value of the same column is associated with a UUID code to uniquely identify it, and two data sets are taken: the one on the left, filtering the clustering key with the filter_left_value value , the one on the right filtering by the value filter_right_value; a join of the two data sets is made, taking the partition key plus the rowid field as comparison criteria.
        
        |key|rowid|value1|value2|
        |---|---|---|---|
        |firstName|544ca336-2d9c-36bb-8433-17371498d2fe|Picasso|Pablo|
        |firstName|f1c25492-21b1-314a-8218-75da2d4e8fbd|Rodin|Auguste|
        |firstName|f1c25492-21b1-314a-8218-1608134e5815|Velazquez|Diego|

    - `stack_p_key` represents partition key.
    - `stack_c_key` is the clustering key
    - `stack_pair` that is a generated field, infers unique pairs from undetermined number of values
    in a row. It will be part of clustering key in the final table.
    - `filter_left_value`, only for `double-value` strategy, pair values related by this value, to put together in the same row.
    - `filter_right_value`, only for `double-value` strategy, pair values related by this value, to put together in the same row.


> Test Details
> People from mock_data table who is older than 40 years old and grouped by age with count aggregation.
> Age is calculated from `birth_date` field, indicated by `calculated` clause.

- Shell snippet

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

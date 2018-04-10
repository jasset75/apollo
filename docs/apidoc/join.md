## Join [/join]

### Join [POST]

Retrieve data from two Cassandra data sets and join them by key fields. It accepts two kind of parameters: simple table description that is an operand; or an operation, two choices also: recursive join description or a recursive union description, which both are composed of two parameters: 

- left operand: table description, join description or union description.
- right operand: table description, join description or union description.

||Possible combinations ||
|:--|:--:|:---|
| table_a |&#10781;|table_b |
| table_a |&#10781;|join_b  |
| table_a |&#10781;|union_b |
| join_a  |&#10781;|table_b |
| join_a  |&#10781;|join_b  |
| join_a  |&#10781;|union_b |
| union_a |&#10781;|table_b |
| union_a |&#10781;|join_b  |
| union_a |&#10781;|union_b |

Thus, recursivelly we could define whatever table merging. Similar to SQL but only binary operations, same functionality.

These descriptions has a few parameters which identify the data source: `keyspace` and `tablename`. Besides that, two descriptions involved in a join operation needs `join_key` parameter that declare which fields are the key to join each other.

Parameters:

- `join_type`, defines kind of Natural Join; in BNF notation:
```
<join_type> ::= "join_type": "inner" | "full" | "left" | "right" | "cross"
```
Optional parameter, `"inner"` is the default value.

Other optional parameters are aimed to apply DML functionality: `groupby`, `select`, `calculated`, etc.:

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

> Test Details
> Ordered list of countries with more than 10K billion Euros of drug annual budget. It summarizes Drug Companies annual budget grouped by country.

- Shell snippet

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
    }'
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
    "orient_results": "columns",
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

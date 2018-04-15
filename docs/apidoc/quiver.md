[< Back](../index.md)

- Group by Clause

    - Aggregations, allowed funcs:
        - max: returns the maximum value of the expression in a group.
        - min: returns the minimum value of the expression in a group.
        - count: returns the number of items in a group.
        - sum: returns the sum of all values in the expression.
        - avg: returns the average of the values in a group.
        - mean: returns the average of the values in a group.
        - sumDistinct: returns the sum of distinct values in the expression.

    ```python
    _agg_allowed_funcs = {
        'max': func.max,
        'min': func.min,
        'count': func.count,
        'sum': func.sum,
        'avg': func.avg,
        'mean': func.mean,
        'sumDistinct': func.sumDistinct
    }
    ```


- Auxiliary Functions

    - `_list_from_list_or_value`

    Returns a list, regardless of the value is `string` or `list`.

    ```python
    def _list_from_list_or_value(value):
    ```

    - `_rename_column`

    Given a dataset, renames column named `name` with `alias` name.

    ```python
    def _rename_column(dataset, name, alias):
    ```

    - `_formatted`
    Internal helper that returns dataset into dict structure.

    ```python
    def _formatted(dataset, format='dict', orient_results='columns'):
    ```

    - `_save`
    Cassandra _write-back_

    ```python
    def _save(ds_table, save):
    ```

    - `_sort_by`
    Sort by clause: parses a sort by clause and applies it over dataset.

    ```python
    def _sort_by(ds_table, sortby):
    ```

    - `_field_or_alias`
    Returns value from value or `{ key: value }`.

    ```python
    def _field_or_alias(term):
    ````

    - `_get_term_key`
    Gets str or key from list of value or `{ key: value }`.

    ```python
    def _get_term_key(term):
    ```

    - `_get_term_value`
    Gets `string` or `value` from list of value or `{ key: value }`

    ```python
    def _get_term_value(term):
    ```

    - `_exists_key` 
    Checks if a key exists in a list of `string` or `{ k: v }`

    ```python
    def _exists_key(ukey, klist):
    ```

    - `_include`

    Include all `list_1` terms: `string` or `{ k: v }` into `list_2` if not exists.

    ```python
    def _include(list_1, list_2):
    ```

    - `_select`
    Select clause always execute before join_key statement with another table; in other words: select values are
    possible keys for join. If not `select` but `join_key`, all fields are select and include `join_key`.

    ```python
    def _select(ds_table, select, join_key):
    ```

    - `_group_by`
    Group by clause:
        
        Parses a group by clause and applies it over dataset.

    ```python
    def _group_by(ds_table, groupby, join_key=None):
    ```

    - `_join_key_building`
    Generates ds_table_a.key_a == ds_table_b.key_b
    with all keys in a single or multiple key join
    When left and right field names are equals, it just removes them,
    thus avoiding duplicate column names.

    ```python
    def _join_key_building(ds_table_a, join_key_a, ds_table_b, join_key_b):
    ```

    - `_map_stack`
    Converts one row columns new rows, keeping keys in all rows,
    and makes new pair unique identifier in order to join related columns

    ```python
    def _map_stack(h_row, stack_p_key, primary_key):
    ```

    - `_go_stacked `
    Given `primary_key` (`partition_key` plus `clustering_key`) and `stack_p_key` (partition key normally) changes the shape of the dataset from n-value columns to n/2 rows. It adds pair key to uniqueness.
    With double-value strategy, one antecedent stack_column is related with other consecuent stack_column by `filter_field`. Antecendents are labeled
    by `filter_left_value` and consecuents are labeled by `filter_right_value`:
        
    ```python
    def _go_stacked(dataset, strategy, stack_p_key, primary_key, stack_pair, stack_column,
                    filter_field, filter_left_value, filter_right_value):
    ```

    - `_stack`
    Gets parameters for stacked operation and launch internal stacking helper function.

    ```python
    def _stack(dataset, keyspace=None, tablename=None, strategy='double-value',
               auto=False, stack_p_key='key', stack_c_key='num', stack_pair='pair',
               stack_column='column', filter_field=None, filter_left_value=None,
               filter_right_value=None):
    ```

    - `_get_table`
    Gets data table from Cassandra. Accept different options:

        - `select`
        - `join`
        - `groupby`
        - `sortby`
        - `calculated`
        - `save`
        - `stacked`

    ```python
    def _get_table(keyspace, tablename, select=None, calculated=None,
                   s_filter=None, groupby=None, sortby=None, join_key=None,
                   save=None, stacked=None):
    ```

    - `_resolve_operand`
    Unpacks operands and calls to specific helper.  This function is quite useful in tree recursion. It calls specific function to operands in defined structure.

    ```python
    def _resolve_operand(table, join, union):
    ```

    - `_trim_str`
    Customizable behavior to filter prefix (i.e. Web Sematic RDF prefix), specially in development environment in order to fit data structures within console width, hardcopy, etc.

    ```python
    def _trim_str(in_str):
    ```

    - `_join`

    Makes a join between two tables. This is a recursive function which explores json structure and resolve in the right way.

    ```python
    def _join(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
              union_b=None, select=None, calculated=None, s_filter=None,
              join_groupby=None, sortby=None, join_key=None, save=None,
              join_type='inner', orient_results='columns'):
    ```

    - `_union`
    Makes a union between two tables. This is a recursive function which explores json structure and resolve in the right way.

    ```python
    def _union(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
               union_b=None, select=None, calculated=None, s_filter=None,
               union_groupby=None, sortby=None, join_key=None, save=None,
               union_type='union_all'):
    ```

- Main Functions

    + Get Table function `get_table`

    This function takes data from a table with optional parameters. It is the stub of `/get-table` API endpoint.

    `orient_results` defines output format
        - split : dict like {index -> [index], columns -> [columns], data -> [values]}
        - records : list like [{column -> value}, ... , {column -> value}]
        - index : dict like {index -> {column -> value}}
        - columns : dict like {column -> {index -> value}}
        - values : just the values array            

    ```python
    def get_table(keyspace, tablename, select=None, calculated=None, s_filter=None, groupby=None, sortby=None,
        join_key=[], format='dict', save=None, stacked=False, orient_results='columns'):
    ```

    + Join function `join`

    This function computes join between operands. It is the stub of `/join` API endpoint.

        * Join Type function `join_type`
        
        This parameter identify
        
            + `"inner"`
            + `"outer"` <=> `"full"` <=> `"fullouter"` <=> `"full_outer"`
            + `"leftouter"` <=> `"left"` <=> `"left_outer"`
            + `"rightouter"` <=> `"right"` <=> `"right_outer"`
            + `"leftsemi"` <=> `"left_semi"`
            + `"leftanti"` <=> `"left_anti"`
            + `"cross"`

        * Format parameter `format`

            `"dict"` or `"str"` (json serialized)

        * Orient Results parameter `orient_results`

        ```
        "split" : dict like {
            index -> [index], 
            columns -> [columns], 
            data -> [values]
        }

        "records" : list like [
            {column -> value},
            ... ,
            {column -> value}
        ]

        "index" : dict like 
        {
            index -> {
                column -> value
            }
        }

        "columns" : dict like 
        {
            column -> {
                index -> value
            }
        }

        "values" : just the values array
        ```

        ```python
        def join(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None, union_b=None, 
            calculated=None, select=None, s_filter=None, join_groupby=None, sortby=None, join_key=[],
            save=None, join_type='inner', format='dict', orient_results='columns'):
        ```

    + Union function `union`

    This function computes union between operands. It is the stub of `/union` API endpoint.

        - Union Type parameter `union_type`
            - `"union_all"`
            - `"intersect"`
            - `"minus"`
            - `"xor"`

        - Format parameter `format`
            - `"dict"` or `"str"` (json serialized)

    ```python
    def union(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None, union_b=None, select=None,
              calculated=None, s_filter=None, union_groupby=None, sortby=None, join_key=[], save=None,
              union_type='union_all', format='dict', orient_results='columns'):
    ```

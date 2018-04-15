- aggregations, allowed funcs:
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

```python
def _list_from_list_or_value(value):
    """
        Returns a list, regardless of the value is str or list
    """
```

```python
def _rename_column(dataset, name, alias):
    """
        Given a dataset, renames column named "name"
        with "alias" name
    """
```

```python
def _formatted(dataset, format='dict', orient_results='columns'):
    """
        Internal helper that returns dataset into dict structure
    """
```

```python
def _save(ds_table, save):
    """
        Cassandra write-back
    """
```

```python
def _sort_by(ds_table, sortby):
    """
        Sort by clause:
            parses a sort by clause and applies it over dataset
    """
```

```python
def _field_or_alias(term):
    """
        Auxiliary function:
            returns value from value or {key: value}
    """

```python
def _get_term_key(term):
    """
        Auxiliary function:
            gets str or key from list of value or {key: value}
    """
```

```python
def _get_term_value(term):
    """
        Auxiliary function:
            gets str or value from list of value or {key: value}
    """
```

```python
def _exists_key(ukey, klist):
    """
        Auxiliary function:
            checks if a key exists in a list of str or {k: v}
    """
```

```python
def _include(list_1, list_2):
    """
        Auxiliary function:
            include all list_1 terms: str or {k: v}
            into list_2 if not exists
    """
```

```python
def _select(ds_table, select, join_key):
    """
        Select clause always execute before join_key statement
        with another table; in other words: select values are
        possible keys for join.
        If not select but join_key, all fields are select and
        include join_key.
    """
```

```python
def _group_by(ds_table, groupby, join_key=None):
    """
        Group by clause:
            parses a group by clause and applies it over dataset
    """
```

```python
def _join_key_building(ds_table_a, join_key_a, ds_table_b, join_key_b):
    """
        Generates ds_table_a.key_a == ds_table_b.key_b
        with all keys in a single or multiple key join
        When left and right field names are equals, it just removes them,
        thus avoiding duplicate column names.
    """
```

```python
def _map_stack(h_row, stack_p_key, primary_key):
    """
        Converts one row columns new rows, keeping keys in all rows,
        and makes new pair unique identifier in order to join related columns
    """
```

```python
def _go_stacked(dataset, strategy, stack_p_key, primary_key, stack_pair, stack_column,
                filter_field, filter_left_value, filter_right_value):
    """
        Given all keys (partition_key plus clustering_key normally)
        and stack_p_key (partition key normally) changes the shape of
        the dataset from n-value columns to n/2 rows.
        it adds pair key to uniqueness.
        With double-value strategy, one antecedent stack_column is related with
        other consecuent stack_column by filter_field. Antecendents are labeled
        by filter_left_value and consecuents are labeled by filter_right_value:
        (stack_p_key, stack_pair, stack_column1, stack_column2)
    """
```

```python
def _stack(dataset, keyspace=None, tablename=None, strategy='double-value',
           auto=False, stack_p_key='key', stack_c_key='num', stack_pair='pair',
           stack_column='column', filter_field=None, filter_left_value=None,
           filter_right_value=None):
    """
        Gets parameters for stacked operation and launch
        internal stacking helper function.
    """
```

```python
def _get_table(keyspace, tablename, select=None, calculated=None,
               s_filter=None, groupby=None, sortby=None, join_key=None,
               save=None, stacked=None):
    """
        Gets data table from Cassandra.

        Accept different options:
            select
            join
            groupby
            sortby
            calculated
            save
            stacked
    """
```

```python
def _resolve_operand(table, join, union):
    """
        Unpacks operands and calls to specific helper.
        This function is quite useful in tree recursion
    """
```

```python
def _trim_str(in_str):
    """
        Customizable behavior to filter prefix
        (i.e.: Web Sematic RDF prefix), specially in development environment
        in order to fit data structures within console width, hardcopy, etc.
    """
```

```python
def _join(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
          union_b=None, select=None, calculated=None, s_filter=None,
          join_groupby=None, sortby=None, join_key=None, save=None,
          join_type='inner', orient_results='columns'):
    """
        Makes a join between two tables, join and table, table and join,
        or two joins this is a recursive function which explores json structure
    """
```

```python
def _union(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
           union_b=None, select=None, calculated=None, s_filter=None,
           union_groupby=None, sortby=None, join_key=None, save=None,
           union_type='union_all'):
    """
        makes a union between two tables, join and table, table and join,
        or two joins this is a recursive function which explores json structure
    """
```

```python
def get_table(keyspace, tablename, select=None, calculated=None, s_filter=None,
              groupby=None, sortby=None, join_key=[], format='dict',
              save=None, stacked=False, orient_results='columns'):
    """
        get_table entry point
            this function computes data from a table
        orient_results:
            split : dict like {index -> [index], columns -> [columns], data -> [values]}
            records : list like [{column -> value}, ... , {column -> value}]
            index : dict like {index -> {column -> value}}
            columns : dict like {column -> {index -> value}}
            values : just the values array            
    """
```

```python
def join(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
         union_b=None, calculated=None, select=None, s_filter=None,
         join_groupby=None, sortby=None, join_key=[], save=None,
         join_type='inner', format='dict', orient_results='columns'):
    """
        join function entry point

        join_type:
            "inner",
            "outer" <=> "full" <=> "fullouter" <=> "full_outer"
            "leftouter" <=> "left" <=> "left_outer"
            "rightouter" <=> "right" <=> "right_outer"
            "leftsemi" <=> "left_semi"
            "leftanti" <=> "left_anti"
            "cross"
        format:
            dict or str (json serialized)
        orient_results:
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
            "index" : dict like {index -> {column -> value}}
            "columns" : dict like {column -> {index -> value}}
            "values" : just the values array
    """
```

```python
def union(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
          union_b=None, select=None, calculated=None, s_filter=None,
          union_groupby=None, sortby=None, join_key=[], save=None,
          union_type='union_all', format='dict', orient_results='columns'):
    """
        union function entry point

        union_type:
            "union_all"
            "intersect"
            "minus"
            "xor"
        format:
            dict or str (json serialized)
    """
```

import os

# auxiliary library to unpack operation parameters
from . import unpack_params as unpack

# project configuration wrapper: yaml formatted file
from misc.config import settings as conf

# cassandra managing helper functions
import admix

# pyspark modules
from pyspark import SparkConf
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql import Row

# pyspark functions
import pyspark.sql.functions as func

# uuid generation support
from uuid import NAMESPACE_URL, uuid3

# environment variable with character encoding
os.putenv('PYTHONIOENCODING', conf.app.encoding)

"""
    allowed funcs:
        max:
            returns the maximum value of the expression in a group.
        min:
            returns the minimum value of the expression in a group.
        count:
            returns the number of items in a group.
        sum:
            returns the sum of all values in the expression.
        avg:
            returns the average of the values in a group.
        mean:
            returns the average of the values in a group.
        sumDistinct:
            returns the sum of distinct values in the expression.
"""
_agg_allowed_funcs = {
    'max': func.max,
    'min': func.min,
    'count': func.count,
    'sum': func.sum,
    'avg': func.avg,
    'mean': func.mean,
    'sumDistinct': func.sumDistinct
}

spark_conf = SparkConf().setAll([
    ('spark.executor.memory', conf.spark.executor.memory),
    ('spark.executor.cores', conf.spark.executor.cores),
    ('spark.cores.max', conf.spark.max_cores),
    ('spark.driver.memory', conf.spark.driver.memory)
])

# setting up Cassandra-ready spark session
# ONE consistency level is mandatory in clusters with one node
spark = (
    SparkSession
    .builder
    .appName('SparkCassandraApp')
    .config('spark.cassandra.connection.host', conf.cassandra.host)
    .config('spark.cassandra.connection.port', conf.cassandra.port)
    .config('spark.cassandra.output.consistency.level',
            conf.cassandra.consistency_level)
    .config(conf=spark_conf)
    .master('local[{}]'.format(conf.spark.executor.cores))
    .getOrCreate()
)


# setting error level to coherent threshold
spark.sparkContext.setLogLevel('OFF')

# creating sql spark context
sqlContext = SQLContext(spark.sparkContext)


def _list_from_list_or_value(value):
    """
        Returns a list, regardless of the value is str or list
    """
    if isinstance(value, list):
        return value
    elif isinstance(value, str):
        return [value]
    else:
        raise Exception('type of value not recognized')


def _rename_column(dataset, name, alias):
    """
        Given a dataset, renames column named "name"
        with "alias" name
    """
    columns = dataset.columns
    name_idx = -1
    for idx, item in enumerate(columns):
        if item == name:
            name_idx = idx
            break
    if name_idx > 0:
        columns[name_idx] = {name: alias}
    # returns dataset with new columns
    return dataset.select([x for x in map(_field_or_alias, columns)])


def _formatted(dataset, format='dict'):
    """
        Internal helper that returns dataset into dict structure
        or json format ready to response.
        Internal recursion requires dict format, but response to client
        requires json serialization.
    """
    # convertion to pandas
    pdf = dataset.toPandas()
    # returning results
    if format == 'dict':
        return pdf.to_dict()
    elif format == 'json':
        return pdf.to_json()
    else:
        raise Exception('Internal Error: Unknow format {0}.'.format(format))


def _save(ds_table, save):
    """
        Cassandra write-back
    """
    if save:
        msave = unpack.save(save)

        (ds_table.write
            .mode('append')
            .format('org.apache.spark.sql.cassandra')
            .options(keyspace=msave["keyspace"], table=msave["tablename"])
            .save())

    return ds_table


def _sort_by(ds_table, sortby):
    """
        Sort by clause:
            parses a sort by clause and applies it over dataset
    """
    if sortby:
        sortBy_columns = []
        for sb in sortby:
            [(k, v)] = sb.items()
            if v == 'desc':
                sortBy_columns.append(func.desc(k))
            else:
                sortBy_columns.append(func.asc(k))
        ds_table = ds_table.sort(*sortBy_columns)
    return ds_table


def _field_or_alias(term):
    """
        Auxiliary function:
            returns value from value or {key: value}
    """
    if isinstance(term, dict):
        [(k, v)] = term.items()
        return func.col(k).alias(v)
    else:
        return func.col(term)


def _get_term_key(term):
    """
        Auxiliary function:
            gets str or key from list of value or {key: value}
    """
    if isinstance(term, dict):
        [(k, v)] = term.items()
        return k
    else:
        return term


def _get_term_value(term):
    """
        Auxiliary function:
            gets str or value from list of value or {key: value}
    """
    if isinstance(term, dict):
        [(k, v)] = term.items()
        return v
    else:
        return term


def _exists_key(ukey, klist):
    """
        Auxiliary function:
            checks if a key exists in a list of str or {k: v}
    """
    for key in klist:
        if ukey == _get_term_value(key):
            return True

    return False


def _include(list_1, list_2):
    """
        Auxiliary function:
            include all list_1 terms: str or {k: v}
            into list_2 if not exists
    """
    if not list_2:
        return list_1
    else:
        for key in list_1:
            value = _get_term_value(key)
            if not _exists_key(value, list_2):
                list_2.append(key)
        return list_2


def _select(ds_table, select, join_key):
    """
        Select clause always execute before join_key statement
        with another table; in other words: select values are
        possible keys for join.
        If not select but join_key, all fields are select and
        include join_key.
    """
    if join_key and not select:
        select = ds_table.columns

    if select:
        if join_key:
            select = _include(join_key, select)
        fields = map(_field_or_alias, select)
        ds_table = ds_table.select(*fields)

    return ds_table


def _group_by(ds_table, groupby, join_key=None):
    """
        Group by clause:
            parses a group by clause and applies it over dataset
    """
    if groupby:
        columns = []
        # list of columns grouped
        grouped = groupby.get('grouped', None)
        # union two lists of fields: join_key and grouped
        if join_key:
            grouped = _include(join_key, grouped)
        # parsing aggregated fields
        agg = groupby.get('agg', None)

        for key, val in agg.items():
            # key is the operator and value is the list of columns
            f_operator = _agg_allowed_funcs.get(key, None)
            if not f_operator:
                raise Exception("Unknown or missing aggragate operator {0}"
                                .format(key))
            for v in val:
                if isinstance(v, dict):
                    columns.append(
                        f_operator(_get_term_key(v)).alias(_get_term_value(v))
                    )
                elif isinstance(v, str):
                    columns.append(f_operator(v))

        ds_table = ds_table.groupby(*grouped).agg(*columns)

    return ds_table


def _join_key_building(ds_table_a, join_key_a, ds_table_b, join_key_b):
    """
        Generates ds_table_a.key_a == ds_table_b.key_b
        with all keys in a single or multiple key join
        When left and right field names are equals, it just removes them,
        thus avoiding duplicate column names.
    """
    # initialize join keys
    join_clause = []
    # compares left term's value with right term's value
    zip_join = zip(
        map(_get_term_value, join_key_a),
        map(_get_term_value, join_key_b)
    )
    for key in zip_join:
        if key[0] == key[1]:
            join_clause.append(key[0])
        else:
            join_clause.append(ds_table_a[key[0]] == ds_table_b[key[1]])

    return join_clause


def _map_stack(h_row, stack_p_key, all_keys):
    """
        Converts one row columns new rows, keeping keys in all rows,
        and makes new pair unique identifier in order to join related columns
    """
    columns = {}
    # uuid seed
    stack_p_key_value = {}
    # common elements
    for idx, key in enumerate(all_keys):
        if key in stack_p_key:
            stack_p_key_value[key] = h_row[idx]
        columns[key] = _trim_str(h_row[idx])
    # stack elements
    return [
        Row(
            **columns,
            quiver_pair_=str(uuid3(NAMESPACE_URL, '{}_{}'.format(str(stack_p_key_value), indx))),
            # quiver_pair is a hash value for elements (columns) of the same key and column position
            # from the original dataset, so it must be part of the key to join elements associated
            # to the previous dataset's key plus column index
            quiver_column_=_trim_str(val)
        ) for indx, val in enumerate(h_row[len(all_keys):])  # iterates over data columns
    ]


def _go_stacked(dataset, strategy, stack_p_key, all_keys, stack_pair, stack_column,
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
    # value name
    _column = 'quiver_column_'
    # pair name
    _pair = 'quiver_pair_'

    # stack main part
    rdd = dataset.rdd.flatMap(
        lambda row: _map_stack(row, stack_p_key, all_keys)
    )

    # renames internal names to definitive names
    df_stacked = _rename_column(
        _rename_column(
            spark.createDataFrame(rdd), _pair, stack_pair
        ), _column, stack_column
    )
    # different strategies implementation
    if strategy == 'single-value':
        return df_stacked
    elif strategy == 'double-value':
        # spliting results between stack_column1 and stack_column2
        df_left = df_stacked.filter(
            df_stacked[filter_field] == func.lit(filter_left_value)
        )
        df_right = df_stacked.filter(
            df_stacked[filter_field] == func.lit(filter_right_value)
        )
        # building the new column shape
        all_keys.remove(filter_field)
        new_columns_1 = all_keys+[
            stack_pair, {stack_column: '{}{}'.format(stack_column, 1)}
        ]
        new_columns_2 = [
            stack_pair, {stack_column: '{}{}'.format(stack_column, 2)}
        ]
        # join preparation
        df_left = df_left.select(
            [col for col in map(_field_or_alias, new_columns_1)]
        )
        df_right = df_right.select(
            [col for col in map(_field_or_alias, new_columns_2)]
        )
        # final joined dataset
        return df_left.join(df_right, stack_pair)


def _stack(dataset, keyspace=None, tablename=None, strategy='double-value',
           auto=False, stack_p_key='key', stack_c_key='num', stack_pair='pair',
           stack_column='column', filter_field=None, filter_left_value=None,
           filter_right_value=None):
    """
        Gets parameters for stacked operation and launch
        internal stacking helper function.
    """
    if strategy not in ['single-value', 'double-value']:
        raise Exception('stack::{} strategy not implemmented'.format(strategy))
    # auto infers stack keys form partition a clustering cassandra groups
    # of keys
    if auto:
        if not keyspace or not tablename:
            raise Exception(
                'stacked::keyspace and tablename are mandatory with auto=true'
            )
        stack_p_key = admix.get_partition_key(keyspace, tablename)
        all_keys = admix.get_all_keys(keyspace, tablename)
    else:
        if not stack_pair or not stack_p_key:
            raise Exception(
                'stacked::stack_p_key and stack_pair are mandatory with auto=false'
            )
        all_keys = _list_from_list_or_value(stack_p_key) + _list_from_list_or_value(stack_c_key)

    return _go_stacked(dataset, strategy, stack_p_key, all_keys, stack_pair, stack_column,
                       filter_field, filter_left_value, filter_right_value)


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
    # dataset creation from Cassandra
    ds_table = (
        sqlContext
        .read
        .format('org.apache.spark.sql.cassandra')
        .options(keyspace=keyspace, table=tablename)
        .load()
    )

    # stacked format configuration
    if stacked:
        mdata = unpack.stacked(stacked)
        mdata['keyspace'] = keyspace
        mdata['tablename'] = tablename
        ds_table = _stack(ds_table, **mdata)

    # any calculated fields
    if calculated:
        for key, val in calculated.items():
            ds_table = ds_table.withColumn(key, func.expr(val))

    # apply select statement
    ds_table = _select(ds_table, select, join_key)

    # filtering records
    if s_filter:
        ds_table = ds_table.filter(s_filter)

    # group by clause
    ds_table = _group_by(ds_table, groupby, join_key)

    # sort by clause
    ds_table = _sort_by(ds_table, sortby)

    # save clause
    _save(ds_table, save)

    # reply dataset with transformation
    return ds_table


def _resolve_operand(table, join, union):
    """
        Unpacks operands and calls to specific helper.
        This function is quite useful in tree recursion
    """
    # left operand
    if table:
        mdata = unpack.table(table)
        ds_table = _get_table(**mdata)
    elif join:
        mdata = unpack.join(join)
        ds_table = _join(**mdata)
    elif union:
        mdata = unpack.union(union)
        ds_table = _union(**mdata)
    else:
        raise Exception('At least *join* or *table* must be defined as '
                        + '*a* operand to join operator.')

    return ds_table, mdata


def _trim_str(in_str):
    """
        Customizable behavior to filter prefix
        (i.e.: Web Sematic RDF prefix), specially in development environment
        in order to fit data structures within console width, hardcopy, etc.
    """
    if conf.app.trim_str:
        if isinstance(in_str, str):
            terms = in_str.split('#')
            if len(terms) == 1:
                return in_str
            else:
                return terms[1]
    return in_str


def _join(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
          union_b=None, select=None, calculated=None, s_filter=None,
          join_groupby=None, sortby=None, join_key=None, save=None,
          join_type='inner'):
    """
        Makes a join between two tables, join and table, table and join,
        or two joins this is a recursive function which explores json structure
    """
    # left operand resolution
    ds_table_a, mdata_a = _resolve_operand(table_a, join_a, union_a)

    # right operand resolution
    ds_table_b, mdata_b = _resolve_operand(table_b, join_b, union_b)

    # join_key list of two operands must be congruent
    if len(mdata_a['join_key']) != len(mdata_b['join_key']):
        raise Exception("""
            join keys must be congruent in length: join_key a {}, join_key b {}
        """.format(mdata_a, mdata_b).strip())

    # prepare join keys compararison
    join_clause = _join_key_building(
        ds_table_a, mdata_a['join_key'], ds_table_b, mdata_b['join_key']
    )

    # nuts and bolts
    ds_join = (
        ds_table_a.join(
            ds_table_b,
            join_clause,
            join_type
        )
    )

    # any calculated fields
    if calculated:
        for key, val in calculated.items():
            ds_join = ds_join.withColumn(key, func.expr(val))

    # apply select statement
    ds_join = _select(ds_join, select, join_key)

    # filtering records
    if s_filter:
        ds_join = ds_join.filter(s_filter)

    # group by clause
    ds_join = _group_by(ds_join, join_groupby, join_key)

    # sort by clause
    ds_join = _sort_by(ds_join, sortby)

    # save clause
    _save(ds_join, save)

    # final datase
    return ds_join


def _union(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
           union_b=None, select=None, calculated=None, s_filter=None,
           union_groupby=None, sortby=None, join_key=None, save=None,
           union_type='union_all'):
    """
        makes a union between two tables, join and table, table and join,
        or two joins this is a recursive function which explores json structure
    """

    # left operand resolution
    ds_table_a, mdata_a = _resolve_operand(table_a, join_a, union_a)

    # right operand resolution
    ds_table_b, mdata_b = _resolve_operand(table_b, join_b, union_b)

    # join_key list of two operands must be congruent
    if len(mdata_a['join_key']) != len(mdata_b['join_key']):
        raise Exception("""
            join keys must be congruent in length: join_key a {}, join_key b {}
        """.format(mdata_a, mdata_b).strip())

    # nuts and bolts
    if union_type == 'union_all':
        ds_union = ds_table_a.unionAll(ds_table_b)
    elif union_type == 'intersect':
        ds_union = ds_table_a.intersect(ds_table_b)
    elif union_type == 'except':
        ds_union = ds_table_a.minus(ds_table_b)
    elif union_type == 'xor':
        ds_union = (
            ds_table_a.unionAll(ds_table_b).minus(
                ds_table_a.intersect(ds_table_b)
            )
        )
    else:
        raise Exception('Union type unknown: {}'.format(union_type))

    # any calculated fields
    if calculated:
        for key, val in calculated.items():
            ds_union = ds_union.withColumn(key, func.expr(val))

    # apply select statement
    ds_union = _select(ds_union, select, join_key)

    # filtering records
    if s_filter:
        ds_union = ds_union.filter(s_filter)

    # group by clause
    ds_union = _group_by(ds_union, union_groupby, join_key)

    # sort by clause
    ds_union = _sort_by(ds_union, sortby)

    # save clause
    _save(ds_union, save)

    # final datase
    return ds_union


def get_table(keyspace, tablename, select=None, calculated=None, s_filter=None,
              groupby=None, sortby=None, join_key=[], format='dict',
              save=None, stacked=False):
    """
        get_table entry point
            this function computes data from a table
    """

    # retrieving dataset from Cassandra
    ds_table = _get_table(keyspace, tablename, select=select,
                          calculated=calculated, s_filter=s_filter,
                          groupby=groupby, sortby=sortby, join_key=join_key,
                          save=save, stacked=stacked)

    return _formatted(ds_table, format)


def join(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
         union_b=None, calculated=None, select=None, s_filter=None,
         join_groupby=None, sortby=None, join_key=[], save=None,
         join_type='inner', format='dict'):
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
    """

    ds_join = _join(table_a=table_a, table_b=table_b, join_a=join_a,
                    join_b=join_b, union_a=union_a, union_b=union_b,
                    select=select, calculated=calculated, s_filter=s_filter,
                    join_groupby=join_groupby, sortby=sortby,
                    join_key=join_key, save=save, join_type=join_type)

    return _formatted(ds_join, format)


def union(table_a=None, table_b=None, join_a=None, join_b=None, union_a=None,
          union_b=None, select=None, calculated=None, s_filter=None,
          union_groupby=None, sortby=None, join_key=[], save=None,
          union_type='union_all', format='dict'):
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
    ds_union = _union(table_a=table_a, table_b=table_b, join_a=join_a,
                      join_b=join_b, union_a=union_a, union_b=union_b,
                      select=select, calculated=calculated, s_filter=s_filter,
                      union_groupby=union_groupby, sortby=sortby,
                      join_key=join_key, save=save, union_type=union_type)

    return _formatted(ds_union, format)

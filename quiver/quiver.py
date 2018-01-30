import os, sys
from . import unpack_params as unpack
from misc.config import settings as conf

os.putenv('PYTHONIOENCODING',conf.encoding)

# auxiliar library to unpack operation parameters


from cassandra.cluster import Cluster

# pyspark modules
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, SparkSession

# pyspark functions
import pyspark.sql.functions as func

def _spark_cassandra_type_mapping(spark_type):
  return ''

def _create_cassandra_table(dataset,keyspace,tablename,partition_key,clustering_key=None,create_if_not_exists=False):
  # checks if creating flag is active
  if create_if_not_exists:
    # Cluster takes ip cluster leader. TO-DO: get from conf
    None


"""
allowed funcs:
  'max': 'Aggregate function: returns the maximum value of the expression in a group.',
  'min': 'Aggregate function: returns the minimum value of the expression in a group.',
  'count': 'Aggregate function: returns the number of items in a group.',
  'sum': 'Aggregate function: returns the sum of all values in the expression.',
  'avg': 'Aggregate function: returns the average of the values in a group.',
  'mean': 'Aggregate function: returns the average of the values in a group.',
  'sumDistinct': 'Aggregate function: returns the sum of distinct values in the expression.'  
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
  ('spark.executor.memory', conf.executor.memory), 
  ('spark.executor.cores', conf.executor.cores), 
  ('spark.cores.max', conf.max_cores),
  ('spark.driver.memory',conf.driver.memory)
])

# setting up Cassandra-ready spark session
# ONE consistency level is mandatory in clusters with one node
spark = (
  SparkSession.builder
    .appName('SparkCassandraApp')
    .config('spark.cassandra.connection.host', conf.cassandra.host)
    .config('spark.cassandra.connection.port', conf.cassandra.port)
    .config('spark.cassandra.output.consistency.level','ONE')
    .config(conf=spark_conf)
    .master('local')
    .getOrCreate()
)  


# setting error level to coherent threshold                
spark.sparkContext.setLogLevel('OFF')

# creating sql spark context
sqlContext = SQLContext(spark.sparkContext)

def _save(ds_table,save):
  if save:
    msave = unpack.save(save)

    _create_cassandra_table(ds_table,**msave)

    (ds_table.write
      .mode('append')
      .format('org.apache.spark.sql.cassandra')
      .options(keyspace = msave["keyspace"], table = msave["tablename"])
      .save())


def _group_by(ds_table,groupby,join_key=None):
  """
    group by clause:
      parses a group by clause and applies it over dataset
  """
  if groupby:
    columns = []
    #list of columns grouped
    grouped = groupby.get('grouped',None)
    # union two lists of fields: join_key and grouped
    if join_key:
      grouped = list(set().union(grouped,map(_get_term_value,join_key)))
    # parsing aggregated fields
    agg = groupby.get('agg',None)
    for key, val in agg.items():
      # key is the operator and value is the list of columns
      f_operator = _agg_allowed_funcs.get(key,None)
      if not f_operator:
        raise Exception("Unknown or missing aggragate operator {0}",key)
      for v in val:
        columns.append(f_operator(v))
    ds_table = ds_table.groupby(*grouped).agg(*columns)
  return ds_table
    
def _sort_by(ds_table,sortby):
  """
    sort by clause:
      parses a sort by clause and applies it over dataset
  """
  if sortby:
    sortBy_columns = []
    for sb in sortby:
      [(k,v)] = sb.items()
      if v == 'desc':
        sortBy_columns.append(func.desc(k))
      else:
        sortBy_columns.append(func.asc(k))
    ds_table = ds_table.sort(*sortBy_columns)
  return ds_table

def _field_or_alias(term):
  """
    auxiliar function:
      returns value from value or {key: value}  
  """
  if isinstance(term,dict):
    [(k,v)] = term.items()
    return func.col(k).alias(v)
  else:
    return func.col(term)

def _get_term_value(term):
  """
    auxiliar function:
      gets str or v from list of value or {key: value}
  """
  if isinstance(term,dict):
    [(k,v)] = term.items()
    return v
  else:
    return term

def _exists_key(ukey,klist):
  """
    auxiliar function:
      checks if a key exists in a list of str or {k: v}
  """
  for key in klist:
    if ukey == _get_term_value(key):
      return True
  return False

def _include(list_1,list_2):
  """
    auxiliar function:
      include all list_1 terms: str or {k: v}
      into list_2 if not exists
  """
  if not list_2:
    return list_1 
  else:
    for key in list_1:
      value = _get_term_value(key)
      if not _exists_key(value,list_2):
        list_2.append(key)
    return list_2

def _select(ds_table,select,join_key):
  """
    select clause always execute before join_key statement
    with another table
    in other words: select values are possible keys for join

    if not select but join_key, all fields are select and include join_key
  """
  if join_key and not select:
    select = ds_table.columns
  if select:
    if join_key:
      select = _include(join_key,select)
    fields = map(_field_or_alias,select)
    ds_table = ds_table.select(*fields)

  return ds_table  

def _get_table(keyspace, tablename, select=None, calculated=None, s_filter=None, groupby=None, sortby=None, join_key=None, save=None):
  """
    Gets data table from Cassandra.

    Accept different options:
      select
      join
      groupby
      sortby
  """
  # dataset creation from Cassandra
  ds_table = (
    sqlContext
      .read
      .format('org.apache.spark.sql.cassandra')
      .options(keyspace=keyspace, table=tablename)
      .load()
  )

  # any calculated fields
  if calculated:
    for key,val in calculated.items():
      ds_table = ds_table.withColumn(key,func.expr(val))

  # apply select statement
  ds_table = _select(ds_table,select,join_key)

  # filtering records
  if s_filter:
    ds_table = ds_table.filter(s_filter)

  # group by clause
  ds_table = _group_by(ds_table,groupby,join_key)

  # sort by clause 
  ds_table = _sort_by(ds_table,sortby)

  # save clause
  _save(ds_table,save)

  # reply dataset with transformation
  return ds_table

def _join(table_a = None, table_b = None, join_a = None, join_b = None, select = None, calculated = None, s_filter = None, join_groupby=None, sortby=None, join_key=None, save=None, join_type='inner'):
  """
    makes a join between two tables, join and table, table and join, or two joins
    this is a recursive function which explores json structure
  """  

  # left operand
  if table_a:
    mdata_a = unpack.table(table_a)
    ds_table_a = _get_table(**mdata_a)
  elif join_a:
    mdata_a = unpack.join(join_a)
    ds_table_a = _join(**mdata_a)
  else:
    raise Exception('At least join or table would be defined as *a* operand to join operator.'.format(format))

  # right operand
  if table_b:
    mdata_b = unpack.table(table_b)
    ds_table_b = _get_table(**mdata_b)
  elif join_b:
    mdata_b = unpack.table(join_b)
  else:
    raise Exception('At least join or table would be defined as *b* operand to join operator.'.format(format))

  # join_key list of two operands must be congruent  
  if len(mdata_a['join_key']) != len(mdata_b['join_key']):
    raise Exception('join keys must be congruent in length: join_key a {}, join_key b {}'.format(mdata_a,mdata_b))

  #prepare join keys
  zip_join = zip(map(_get_term_value,mdata_a['join_key']),map(_get_term_value,mdata_b['join_key']))
  join_clause = []
  for key in zip_join:
    join_clause.append(ds_table_a[key[0]] == ds_table_b[key[1]])

  # nuts and bolts  
  ds_join = (
    ds_table_a
      .join(
        ds_table_b,
        join_clause,
        join_type
      )
  )

  # any calculated fields
  if calculated:
    for key,val in calculated.items():
      ds_join = ds_join.withColumn(key,func.expr(val))

  # apply select statement
  ds_join = _select(ds_join,select,join_key)

  # filtering records
  if s_filter:
    ds_join = ds_join.filter(s_filter)

  # group by clause
  ds_join = _group_by(ds_join,join_groupby,join_key)

  # sort by clause 
  ds_join = _sort_by(ds_join,sortby)

  # save clause
  _save(ds_join,save)

  # final datase
  return ds_join

def _union(table_a = None, table_b = None, join_a = None, join_b = None, union_a = None, union_b = None, select = None, calculated = None, s_filter = None, union_groupby=None, sortby=None, join_key=None, save=None, union_type='union_all'):
  """
    makes a union between two tables, join and table, table and join, or two joins
    this is a recursive function which explores json structure
  """  

  # left operand
  if table_a:
    mdata_a = unpack.table(table_a)
    ds_table_a = _get_table(**mdata_a)
  elif join_a:
    mdata_a = unpack.join(join_a)
    ds_table_a = _join(**mdata_a)
  elif union_a:
    mdata_a = unpack.union(union_a)
    ds_table_a = _union(**mdata_a)
  else:
    raise Exception('At least join, table or union would be defined as *a* operand to join operator.'.format(format))

  # right operand
  if table_b:
    mdata_b = unpack.table(table_b)
    ds_table_b = _get_table(**mdata_b)
  elif join_b:
    mdata_b = unpack.table(join_b)
    ds_table_b = _join(**mdata_b)
  elif union_b:
    mdata_b = unpack.union(union_b)
    ds_table_b = _union(**mdata_b)
  else:
    raise Exception('At least join or table would be defined as *b* operand to join operator.'.format(format))

  # join_key list of two operands must be congruent  
  if len(mdata_a['join_key']) != len(mdata_b['join_key']):
    raise Exception('join keys must be congruent in length: join_key a {}, join_key b {}'.format(mdata_a,mdata_b))

  #prepare join keys
  zip_join = zip(map(_get_term_value,mdata_a['join_key']),map(_get_term_value,mdata_b['join_key']))
  join_clause = []
  for key in zip_join:
    join_clause.append(ds_table_a[key[0]] == ds_table_b[key[1]])

  # nuts and bolts 
  if union_type == 'union_all':
    ds_union = ds_table_a.unionAll(ds_table_b)
  elif union_type == 'intersect':
    ds_union = ds_table_a.intersect(ds_table_b)
  elif union_type == 'except':
    ds_union = ds_table_a.minus(ds_table_b)
  elif union_type == 'xor':
    ds_union = ds_table_a.unionAll(ds_table_b).minus(ds_table_a.intersect(ds_table_b))
  else:
    raise Exception('Union type unknown: {}'.format(union_type))

  # any calculated fields
  if calculated:
    for key,val in calculated.items():
      ds_union = ds_union.withColumn(key,func.expr(val))

  # apply select statement
  ds_union = _select(ds_union,select,join_key)

  # filtering records
  if s_filter:
    ds_union = ds_union.filter(s_filter)

  # group by clause
  ds_union = _group_by(ds_union,union_groupby,join_key)

  # sort by clause 
  ds_union = _sort_by(ds_union,sortby)

  # save clause
  _save(ds_union,save)

  # final datase
  return ds_union

def get_table(keyspace, tablename, select = None, calculated = None, s_filter = None, groupby = None, sortby = None, join_key = [], format = 'dict', save = None):
  """
    get_table entry point
      this function computes data from a table
  """
  # retrieving dataset from Cassandra
  ds_table = _get_table(keyspace, tablename, select, calculated, s_filter, groupby, sortby, join_key)

  # convert to pandas
  pdf = ds_table.toPandas()

  #formatting data
  if format == 'dict':
    return pdf.to_dict()
  elif format == 'json':
    return pdf.to_json()
  else:
    raise Exception('Internal Error: Unknow format {0}.'.format(format))


def join(table_a = None, table_b = None, join_a = None, join_b = None, calculated = None, select = None,
         s_filter=None, join_groupby=None, sortby=None, join_key=[], save=None, join_type='inner', format='dict'):
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
  ds_join = _join(table_a, table_b, join_a, join_b, select, calculated, s_filter, join_groupby, sortby, join_key, save, join_type)

  # convert to pandas
  pdf = ds_join.toPandas()
  # returning results
  if format == 'dict':
    return pdf.to_dict()
  elif format == 'json':
    return pdf.to_json()
  else:
    raise Exception('Internal Error: Unknow format {0}.'.format(format))

def union(table_a = None, table_b = None, join_a = None, join_b = None, union_a = None, union_b = None, calculated = None, select = None,
         s_filter=None, union_groupby=None, sortby=None, join_key=[], save=None, union_type='union_all', format='dict'):
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
  ds_union = _union(table_a, table_b, join_a, join_b, union_a, union_b, select, calculated, s_filter, union_groupby, sortby, join_key, save, union_type)

  # convert to pandas
  pdf = ds_union.toPandas()
  # returning results
  if format == 'dict':
    return pdf.to_dict()
  elif format == 'json':
    return pdf.to_json()
  else:
    raise Exception('Internal Error: Unknow format {0}.'.format(format))

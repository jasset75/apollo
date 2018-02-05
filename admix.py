import os
from misc.config import settings as conf
from cassandra.cluster import Cluster
from cassandra.policies import TokenAwarePolicy, RoundRobinPolicy

from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import Ascii, BigInt, Blob, Bytes, Boolean
from cassandra.cqlengine.columns import Counter, Date, DateTime, Decimal
from cassandra.cqlengine.columns import Double, Float, Integer, List, Map
from cassandra.cqlengine.columns import Set, SmallInt, Text, Time, TimeUUID
from cassandra.cqlengine.columns import TinyInt, UUID, VarInt

from cassandra.cqlengine.management import sync_table, create_keyspace_simple

import atexit

# environment variable allow schema management
os.putenv('CQLENG_ALLOW_SCHEMA_MANAGEMENT', 'CQLENG_ALLOW_SCHEMA_MANAGEMENT')

# Apache Cassandra connection
list_of_ip = [conf.cassandra.host]
cluster = Cluster(
    list_of_ip,
    load_balancing_policy=TokenAwarePolicy(RoundRobinPolicy()),
    port=conf.cassandra.port
)
session = cluster.connect()
connection.set_session(session)


class TypeException(Exception):
    None


@atexit.register
def quiver_bye():
    print('\nShutting down...')
    session.shutdown()


def _assert_type_exception(value, msg, args=[]):
    if not value:
        raise TypeException(msg.format(*args))


def _str_to_column(type_str, key_type=None, value_type=None, column_def={}):
    """
        Converts name of Cassandra types to driver class wrapper for
        that type.
    """
    type_str = type_str.lower()

    if type_str == 'integer':
        return Integer(**column_def)
    elif type_str == 'text':
        return Text(**column_def)
    elif type_str == 'ascii':
        return Ascii(**column_def)
    elif type_str == 'bigint':
        return BigInt(**column_def)
    elif type_str == 'blob':
        return Blob(**column_def)
    elif type_str == 'bytes':
        return Bytes(**column_def)
    elif type_str == 'boolean':
        return Boolean(**column_def)
    elif type_str == 'counter':
        return Counter(**column_def)
    elif type_str == 'date':
        return Date(**column_def)
    elif type_str == 'datetime':
        return DateTime(**column_def)
    elif type_str == 'decimal':
        return Decimal(**column_def)
    elif type_str == 'double':
        return Double(**column_def)
    elif type_str == 'float':
        return Float(**column_def)
    elif type_str == 'list':
        _assert_type_exception(value_type, "list type requires value_type")
        return List(value_type=value_type, **column_def)
    elif type_str == 'map':
        _assert_type_exception(key_type, "list type requires key_type")
        _assert_type_exception(value_type, "list type requires value_type")
        return Map(key_type=key_type, value_type=value_type, **column_def)
    elif type_str == 'set':
        _assert_type_exception(value_type, "set type requires value_type")
        return Set(value_type=value_type, **column_def)
    elif type_str == 'smallint':
        return SmallInt(**column_def)
    elif type_str == 'time':
        return Time(**column_def)
    elif type_str == 'timeuuid':
        return TimeUUID(**column_def)
    elif type_str == 'timestamp':
        return TimeUUID(**column_def)
    elif type_str == 'tinyint':
        return TinyInt(**column_def)
    elif type_str == 'uuid':
        return UUID(**column_def)
    elif type_str == 'varint':
        return VarInt(**column_def)
    else:
        raise Exception('Type {} is not defined.'.format(type_str))


def _build_fields(keyspace, tablename, columns_def):

    # create copy to no modify original
    columns = [{**col} for col in columns_def]

    fields = dict(
      __keyspace__=keyspace,
      __table_name__=tablename
    )

    for column in columns:
        # db_type doesn't be passet to Column __init__
        str_type = column.pop('db_type', 'Text')
        col_name = column['db_field']
        str_key_type = column.pop('key_type', None)
        str_value_type = column.pop('value_type', None)

        # column type inference
        if str_key_type and str_value_type:
            key_type = _str_to_column(str_key_type)
            value_type = _str_to_column(str_value_type)
            fields[col_name] = _str_to_column(
                str_type, key_type=key_type,
                value_type=value_type, column_def=column
            )
        elif str_value_type:
            value_type = _str_to_column(str_value_type)
            fields[col_name] = _str_to_column(
                str_type, value_type=value_type, column_def=column
            )
        else:
            fields[col_name] = _str_to_column(str_type, column_def=column)

    return fields


def create_table(keyspace, tablename, columns, partition_key=None,
                 cluster_key=None, replication_factor=1,
                 durable_writes=True, connections=None):

    create_keyspace_simple(
        keyspace,
        replication_factor,
        durable_writes=durable_writes,
        connections=connections)

    fields = _build_fields(keyspace, tablename, columns)
    metaClass = type('MetaClass', (Model, object), fields)

    sync_table(metaClass)


if __name__ == '__main__':
    columns = [
        dict(db_field='uno', db_type='Integer', primary_key=True),
        dict(db_field='dos')
    ]

    create_table('test_keyspace', 'table_new', columns)

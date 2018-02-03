import os
from misc.config import settings as conf
from cassandra.cluster import Cluster
from cassandra.policies import TokenAwarePolicy, RoundRobinPolicy

from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import Text, Integer
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


@atexit.register
def quiver_bye():
    print("\nShutting down...")
    session.shutdown()


def _str_to_column(str, column_def):
    if str == "Integer":
        return Integer(**column_def)
    if str == "Text":
        return Text(**column_def)


def create_table(keyspace, tablename, columns, partition_key=None,
                 cluster_key=None, replication_factor=1,
                 durable_writes=True, connections=None):

    fields = dict(
      __keyspace__=keyspace,
      __table_name__=tablename
    )

    for column in columns:
        str_type = column.pop("db_type", "Text")
        col_name = column["db_field"]
        fields[col_name] = _str_to_column(str_type, column)

    create_keyspace_simple(
        keyspace,
        replication_factor,
        durable_writes=durable_writes,
        connections=connections)

    metaClass = type("MetaClass", (Model, object), fields)

    sync_table(metaClass)


if __name__ == '__main__':
    columns = [
        dict(db_field='uno', db_type="Integer", primary_key=True),
        dict(db_field='dos')
    ]

    create_table('test_keyspace', 'table_new', columns)

[< Back](../index.md)

- `get_keyspaces`

Returns a list of strings representing each keyspaces of Cassandra 
(similar to cql command `describe keyspaces;`)

```python
def get_keyspaces():
```

- `get_tablenames`

Gets a table list of `keyspace`

```python
def get_tablenames(keyspace):
```

- `get_columns`

Returns a list of columns from keyspace.tablename

```python
def get_columns(keyspace, tablename):
```

- `get_partition_key`

Gets partition key from keyspace.tablename

```python
def get_partition_key(keyspace, tablename):
```

- `get_clustering_key`

Gets clustering key from keyspace.tablename

```python
def get_clustering_key(keyspace, tablename):
```

- `get_primary_key`

Gets primary key

```python
def get_primary_key(keyspace, tablename):
```

- `describe_table`

Describe keyspace.tablename

```python
def describe_table(keyspace, tablename):
```

- `create_keyspace`

Creates a keyspace with keyspace name, strategy and replication_factor are regular
options for Cassandra Keyspaces, see documentation at 
[Datastax](https://docs.datastax.com/en/cql/3.3/cql/cql_reference/cqlCreateKeyspace.html)

```python
def create_keyspace(keyspace, strategy='SimpleStrategy', replication_factor=1):
```

- `create_table`

Creates a table with keyspade.tablename
columns parameter has a dictionary description for data fields

```python
def create_table(keyspace, tablename, columns, partition_key=None,
                 cluster_key=None, replication_factor=1,
                 durable_writes=True, connections=None, create_keyspace_if_not_exists=True):
```

```python
def get_keyspaces():
    '''
    returns a list of strings representing each keyspaces of Cassandra 
    (similar to cql command `describe keyspaces;`)
    '''
```

```python
def get_tablenames(keyspace):
    '''
    gets a table list of `keyspace`
    '''
```

```python

def get_columns(keyspace, tablename):
    '''
    returns a list of columns from keyspace.tablename
    '''
```

```python

def get_partition_key(keyspace, tablename):
    '''
    gets partition key from keyspace.tablename
    '''
```

```python
def get_clustering_key(keyspace, tablename):
    '''
    gets clustering key from keyspace.tablename
    '''
```

```python
def get_primary_key(keyspace, tablename):
    '''
    gets primary key
    '''
```

```python
def describe_table(keyspace, tablename):
    '''
    describe keyspace.tablename
    '''
```

```python
def create_keyspace(keyspace, strategy='SimpleStrategy', replication_factor=1):
    '''
    creates a keyspace with keyspace name, strategy and replication_factor are regular
    options for Cassandra Keyspaces, see Datastax documentation at 
    https://docs.datastax.com/en/cql/3.3/cql/cql_reference/cqlCreateKeyspace.html
    '''
```

```python
def create_table(keyspace, tablename, columns, partition_key=None,
                 cluster_key=None, replication_factor=1,
                 durable_writes=True, connections=None, create_keyspace_if_not_exists=True):
    '''
    Creates a table with keyspade.tablename
    columns parameter has a dictionary description for data fields
    '''
```

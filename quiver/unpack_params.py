def table(table_json):
  metadata = {}
  metadata['keyspace'] = table_json.get('keyspace',None)
  metadata['tablename'] = table_json.get('tablename',None)
  metadata['calculated'] = table_json.get('calculated',None)
  metadata['s_filter'] = table_json.get('filter',None)
  metadata['select'] = table_json.get('select',None)
  metadata['groupby'] = table_json.get('groupby',None)
  metadata['sortby'] = table_json.get('sortby',None)
  metadata['join_key'] = table_json.get('join_key',None)
  metadata['save'] = table_json.get('save',None)
  return metadata

def join(join_json):
  metadata = {}
  metadata['table_a'] = join_json.get('table_a',None)
  metadata['table_b'] = join_json.get('table_b',None)
  metadata['join_a'] = join_json.get('join_a',None)
  metadata['join_b'] = join_json.get('join_b',None)
  metadata['calculated'] = join_json.get('calculated',None)
  metadata['select'] = join_json.get('select',None)
  metadata['s_filter'] = join_json.get('filter',None)
  metadata['join_groupby'] = join_json.get('groupby',None)
  metadata['sortby'] = join_json.get('sortby',None)
  metadata['join_type'] = join_json.get('join_type',None)
  metadata['join_key'] = join_json.get('join_key',None)
  return metadata

def save(save_json):
  metadata = {}
  metadata['keyspace'] = save_json.get('keyspace',None)
  metadata['tablename'] = save_json.get('tablename',None)
  metadata['partition_key'] = save_json.get('partition_key',None)
  return metadata


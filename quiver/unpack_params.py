def table(table_json):

    metadata = {}
    metadata['keyspace'] = table_json.get('keyspace', None)
    metadata['tablename'] = table_json.get('tablename', None)
    metadata['calculated'] = table_json.get('calculated', None)
    metadata['s_filter'] = table_json.get('filter', None)
    metadata['select'] = table_json.get('select', None)
    metadata['groupby'] = table_json.get('groupby', None)
    metadata['sortby'] = table_json.get('sortby', None)
    metadata['join_key'] = table_json.get('join_key', [])
    metadata['save'] = table_json.get('save', None)
    metadata['stacked'] = table_json.get('stacked', None)
    metadata['orient_results'] = table_json.get('orient_results', 'columns')

    return metadata


def join(join_json):

    metadata = {}
    metadata['table_a'] = join_json.get('table_a', None)
    metadata['table_b'] = join_json.get('table_b', None)
    metadata['join_a'] = join_json.get('join_a', None)
    metadata['join_b'] = join_json.get('join_b', None)
    metadata['union_a'] = join_json.get('union_a', None)
    metadata['union_b'] = join_json.get('union_b', None)
    metadata['calculated'] = join_json.get('calculated', None)
    metadata['select'] = join_json.get('select', None)
    metadata['s_filter'] = join_json.get('filter', None)
    metadata['join_groupby'] = join_json.get('groupby', None)
    metadata['sortby'] = join_json.get('sortby', None)
    metadata['join_type'] = join_json.get('join_type', 'inner')
    metadata['join_key'] = join_json.get('join_key', [])
    metadata['save'] = join_json.get('save', None)
    metadata['orient_results'] = join_json.get('orient_results', 'columns')

    return metadata


def union(union_json):

    metadata = {}
    metadata['table_a'] = union_json.get('table_a', None)
    metadata['table_b'] = union_json.get('table_b', None)
    metadata['join_a'] = union_json.get('join_a', None)
    metadata['join_b'] = union_json.get('join_b', None)
    metadata['union_a'] = union_json.get('union_a', None)
    metadata['union_b'] = union_json.get('union_b', None)
    metadata['calculated'] = union_json.get('calculated', None)
    metadata['select'] = union_json.get('select', None)
    metadata['s_filter'] = union_json.get('filter', None)
    metadata['union_groupby'] = union_json.get('groupby', None)
    metadata['sortby'] = union_json.get('sortby', None)
    metadata['union_type'] = union_json.get('union_type', 'union_all')
    metadata['join_key'] = union_json.get('join_key', [])
    metadata['save'] = union_json.get('save', None)
    metadata['orient_results'] = union_json.get('orient_results', 'columns')

    return metadata


def save(save_json):

    metadata = {}
    metadata['keyspace'] = save_json.get('keyspace', None)
    metadata['tablename'] = save_json.get('tablename', None)
    metadata['partition_key'] = save_json.get('partition_key', None)
    metadata['create_if_not_exists'] = \
        save_json.get('create_if_not_exists', None)

    return metadata


def stacked(stacked_json):

    metadata = {}
    metadata['stack_p_key'] = stacked_json.get('stack_p_key', None)
    metadata['stack_c_key'] = stacked_json.get('stack_c_key', None)
    metadata['strategy'] = stacked_json.get('strategy', 'double-value')
    metadata['auto'] = stacked_json.get('auto', False)
    metadata['stack_pair'] = stacked_json.get('stack_pair', 'pair')
    metadata['stack_column'] = stacked_json.get('stack_column', 'columns')
    metadata['filter_field'] = stacked_json.get('filter_field', None)
    metadata['filter_left_value'] = stacked_json.get('filter_left_value', None)
    metadata['filter_right_value'] = stacked_json.get('filter_right_value', None)

    return metadata
